import tkinter as tk

from model import *
from tkinter.filedialog import askdirectory
from os.path import isfile, join
from os import listdir
from PIL import Image, ImageTk
import os
import json
MAX_CANVAS_WIDTH = 1200
MAX_CANVAS_HEIGHT = 600
PANEL_WIDTH = 200
TICK = "+"#"\u2713"
CROSS = "-"#"\u274c"

def fichiers_de(nom_dossier):
    return sorted([f for f in listdir(nom_dossier) if isfile(join(nom_dossier, f))])

def nom_associe(nom_photo):
    radical = os.path.splitext(nom_photo)[0]
    nom_json = radical + ".json"
    return nom_json

def est_image(nom_fichier):
    extension = os.path.splitext(nom_fichier)[1]
    extension = extension.lower()
    return extension in [".tiff", ".gif", ".png", ".jpg", ".jpeg"]

class App(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.rectangles = []
        self.liste_fichiers = []
        self.indice_rectangle_actuel = None
        self.rectangle_en_cours = None
        self.indice_photo_actuelle = None
        self.est_sauvegarde = True
        self.init_widgets()
        
    def init_widgets(self):
        self.barre_menu = tk.Frame(self.parent)
        self.barre_menu.grid(row=0, column=0, columnspan=3, sticky="w")

        self.panneau_gauche = tk.Frame(self.parent, width=PANEL_WIDTH)
        self.panneau_gauche.grid(row=1, column=0, sticky="nsew")

        self.zone_centre = tk.Frame(
            self.parent, width=MAX_CANVAS_WIDTH, height=MAX_CANVAS_HEIGHT)
        self.zone_centre.grid(row=1, column=1)
        self.zone_centre.grid_propagate(False)
        self.zone_centre.grid_rowconfigure(0, weight=1)
        self.zone_centre.grid_columnconfigure(0, weight=1)

        self.panneau_droite = tk.Frame(self.parent, width=PANEL_WIDTH)
        self.panneau_droite.grid(row=1, column=2, sticky="nsew")

        self.bouton_ouvrir_dossier = tk.Button(self.barre_menu, text="Ouvrir dossier", command=self.ouvrir_dossier)
        self.bouton_ouvrir_dossier.grid(row=0, column=0)
        self.bouton_enregistrer_rectangles = tk.Button(self.barre_menu, text="Enregistrer rectangles", command=self.enregistrer_rectangles)
        self.bouton_enregistrer_rectangles.grid(row=0, column=1)

        self.label_dossier_ouvert = tk.Label(self.panneau_gauche, text="<Pas de dossier ouvert>")
        self.label_dossier_ouvert.grid(row=0, column=0)
        self.liste_photos = tk.Listbox(self.panneau_gauche)
        self.liste_photos.bind("<<ListboxSelect>>", self.charger_photo_selectionnee)
        self.liste_photos.grid(row=1, column=0, sticky="nsew")

        self.canvas = tk.Canvas(
            self.zone_centre, width=MAX_CANVAS_WIDTH, height=MAX_CANVAS_HEIGHT)
        self.canvas.bind("<Button-1>", self.debut_rectangle)
        self.canvas.bind("<ButtonRelease-1>", self.fin_rectangle)
        self.canvas.bind("<B1-Motion>", self.avance_rectangle)
        self.canvas_image_ref = self.canvas.create_image(0, 0, anchor = tk.NW)
        self.canvas.grid(row=0, column=0)

        self.bouton_supprimer_rectangle = tk.Button(self.panneau_droite, text="Supprimer rectangle", command=self.supprimer_rectangle_selectionne)
        self.bouton_supprimer_rectangle.grid(row=0, column=0)
        self.liste_rectangles = tk.Listbox(self.panneau_droite)
        self.liste_rectangles.bind("<<ListboxSelect>>", self.charger_rectangle_selectionne)
        self.liste_rectangles.grid(row=1, column=0, sticky="nsew")

        self.mettre_a_jour_etat_bouton_enregistrer()

    def ouvrir_dossier(self):
        self.directoryname = askdirectory()
        self.label_dossier_ouvert.configure(text=self.directoryname)
        self.mettre_a_jour_liste_photos()
        self.selectionner_photo_suivante()
        self.charger_photo_selectionnee()
    
    def photos_du_dossier(self):
        self.liste_fichiers = fichiers_de(self.directoryname)
        resultat = []
        for nom_fichier in self.liste_fichiers:
            if est_image(nom_fichier):
                resultat.append((nom_fichier, self.est_deja_traitee(nom_fichier)))
        return resultat

    def enregistrer_rectangles(self):
        chemin_json = nom_associe(self.chemin_photo)
        with open(chemin_json, "w") as fichier_json : 
            json.dump(self.donnees_rectangles(), fichier_json, indent=4)
        self.mettre_a_jour_liste_photos()
        self.selectionner_photo_suivante()
        self.est_sauvegarde = True
        self.mettre_a_jour_etat_bouton_enregistrer()

    def charger_photo_selectionnee(self, *args):
        t = self.liste_photos.curselection()
        if not t:
            return
        self.supprimer_rectangles()
        self.est_sauvegarde = True
        self.mettre_a_jour_etat_bouton_enregistrer()
        self.indice_rectangle_actuel = None
        self.rectangle_en_cours = None
        self.indice_photo_actuelle = t[0]
        nom_photo = self.photos[self.indice_photo_actuelle][0]
        self.chemin_photo = os.path.join(self.directoryname, nom_photo)

        self.image = Image.open(self.chemin_photo)
        if self.image.width > MAX_CANVAS_WIDTH or self.image.height > MAX_CANVAS_HEIGHT :
            self.ratio = max (self.image.width/MAX_CANVAS_WIDTH, self.image.height/MAX_CANVAS_HEIGHT)
            cw = int(self.image.width / self.ratio)
            ch = int(self.image.height / self.ratio)
            self.image = self.image.resize((cw, ch), Image.ANTIALIAS)
        else :
            self.ratio = 1
            cw = self.image.width
            ch = self.image.height
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.canvas.itemconfigure(self.canvas_image_ref, image=self.image_tk)
        self.canvas.configure(width=cw, height=ch)
        self.canvas.update()
        pass
    
    def mettre_a_jour_etat_bouton_enregistrer(self):
        if self.est_sauvegarde : 
            self.bouton_enregistrer_rectangles.config(state = tk.DISABLED)
        else :
            self.bouton_enregistrer_rectangles.config(state = tk.NORMAL)
        # regarder self.est_sauvegarde, et activer / désactiver le bouton enregistrer en fonction
    
    def selectionner_photo(self, indice):
        self.liste_photos.selection_clear(0, tk.END)
        self.liste_photos.selection_set(indice)
        self.liste_photos.see(indice)
        self.liste_photos.activate(indice)
        self.liste_photos.selection_anchor(indice)
        self.charger_photo_selectionnee()
    
    def selectionner_photo_suivante(self):
        n = len(self.photos)
        c = 0  # compteur de combien de photos j'ai examiné
        i = self.indice_photo_actuelle + 1 if self.indice_photo_actuelle is not None else 0 # indice de la photo que j'examine
        while c < n:
            if i == n:
                i = 0
            (nom_photo, deja_faite) = self.photos[i]
            if not deja_faite:
                self.selectionner_photo(i)
                break
            else:
                i += 1
            c += 1 # equiv à c = c + 1
    
    def mettre_a_jour_liste_rectangles(self):
        self.liste_rectangles.delete(0, tk.END)
        for rectangle in self.rectangles :
            texte = "Rect {} ({}, {}, {}, {})".format(rectangle.id, *rectangle.get_coords())
            self.liste_rectangles.insert(tk.END, texte)

    def mettre_a_jour_liste_photos(self):
        self.liste_photos.delete(0, tk.END)
        self.photos = self.photos_du_dossier()
        for nom_photo, deja_fait in self.photos:
            texte = nom_photo + " " + (TICK if deja_fait else CROSS)
            self.liste_photos.insert(tk.END, texte)

    def est_deja_traitee(self, nom_photo):
        return nom_associe(nom_photo) in self.liste_fichiers
    
    def supprimer_rectangles(self):
        for rectangle in self.rectangles:
            self.canvas.delete(rectangle.id)
        self.rectangles = []
        self.mettre_a_jour_liste_rectangles()
        self.liste_rectangles.selection_clear(0, tk.END)

    def supprimer_rectangle_selectionne(self):
        if self.indice_rectangle_actuel is None:
            return
        # ici, on a l'indice du rectangle selectionné dans self.rectangles
        rectangle = self.rectangles[self.indice_rectangle_actuel]
        self.rectangles.pop(self.indice_rectangle_actuel)
        self.canvas.delete(rectangle.id)
        self.indice_rectangle_actuel = None
        n = len(self.rectangles)
        self.mettre_a_jour_liste_rectangles()
        if n > 0:
            self.selectionner_rectangle(n - 1)
            self.est_sauvegarde = False
        else:
            self.est_sauvegarde = True
        self.mettre_a_jour_etat_bouton_enregistrer()

    def charger_rectangle_selectionne(self, *args):
        t = self.liste_rectangles.curselection()
        if not t:
            print("skipped")
            return
        indice_rectangle = t[0]
        self.peindre_rectangle(self.indice_rectangle_actuel, "red")
        self.indice_rectangle_actuel = indice_rectangle
        self.peindre_rectangle(self.indice_rectangle_actuel, "green")

    def peindre_rectangle(self, indice, couleur):
        if indice is None:
            return
        rectangle = self.rectangles[indice]
        self.canvas.itemconfigure(rectangle.id, outline = couleur)


    def selectionner_rectangle(self, indice):
        self.liste_rectangles.selection_clear(0, tk.END)
        self.liste_rectangles.selection_set(indice)
        self.liste_rectangles.see(indice)
        self.liste_rectangles.activate(indice)
        self.liste_rectangles.selection_anchor(indice)
        self.charger_rectangle_selectionne()

    def ajouter_rectangle(self):
        rectangle = self.rectangle_en_cours
        self.rectangle_en_cours = None
        self.rectangles.append(rectangle)
        self.mettre_a_jour_liste_rectangles()
        indice = len(self.rectangles) - 1
        self.est_sauvegarde = False
        self.mettre_a_jour_etat_bouton_enregistrer()
        self.selectionner_rectangle(indice)
    
    def donnees_rectangles(self):
        resultat = []
        for rectangle in self.rectangles:
            resultat.append(rectangle.get_obj(self.ratio))
        return resultat

    def debut_rectangle(self, event):
        self.peindre_rectangle(self.indice_rectangle_actuel, "red")
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        id = self.canvas.create_rectangle(
            x, y, x, y, outline="green", width=2)
        self.rectangle_en_cours = Rect.begin_with(id, x, y)
        print("Rectangle {} commencé à ({}, {})".format(id, x, y))

    def avance_rectangle(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.rectangle_en_cours.update_end_with(x, y)
        self.canvas.coords(self.rectangle_en_cours.id, *self.rectangle_en_cours.get_coords())

    def fin_rectangle(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.rectangle_en_cours.update_end_with(x, y)
        self.canvas.coords(self.rectangle_en_cours.id, *self.rectangle_en_cours.get_coords())
        print("Rectangle {} fini à ({}, {})".format(self.rectangle_en_cours.id, x, y))
        self.ajouter_rectangle()

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
