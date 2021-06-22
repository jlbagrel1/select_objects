import tkinter as tk

from model import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import os
import json
RECT_BORDER_COLOR = "#4eccde"
MAX_CANVAS_WIDTH = 1200
MAX_CANVAS_HEIGHT = 600

class App(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.current_rect = None
        self.rects = []
        self.objs = []
        self.init_widgets()
       


    def init_widgets(self):
        self.canvas = tk.Canvas(
            self.parent, width=900, height=400, bg="white")
        self.canvas.bind("<Button-1>", self.begin_rect)
        self.canvas.bind("<ButtonRelease-1>", self.end_rect)
        self.canvas.bind("<B1-Motion>", self.progress_rect)
        self.cimageref = self.canvas.create_image(0,0, anchor = tk.NW)
        self.canvas.grid(row=1, column=0,columnspan=2, sticky="nsew")
        bouton_ouvrir = tk.Button(self.parent, text ="Ouvrir", command = self.ouvrir)
        bouton_ouvrir.grid(row=0,column=0, padx = 5, pady = 5)
        button_enregistrer = tk.Button(self.parent, text ="Enregistrer", command = self.enregistrer)
        button_enregistrer.grid(row=0,column=1, padx = 5, pady = 5)
    def ouvrir (self):
        self.filename = askopenfilename()
        self.image = Image.open(self.filename)
        if self.image.width > MAX_CANVAS_WIDTH or self.image.height > MAX_CANVAS_HEIGHT :
            self.ratio = max (self.image.width/MAX_CANVAS_WIDTH, self.image.height/MAX_CANVAS_HEIGHT)
            cw = int(self.image.width / self.ratio)
            ch = int(self.image.height / self.ratio)
            self.image = self.image.resize((cw, ch), Image.ANTIALIAS)
        else :
            self.ratio = 1
            cw = self.image.width
            ch = self.image.height
        self.imagetk = ImageTk.PhotoImage(self.image)
        self.canvas.itemconfigure(self.cimageref, image=self.imagetk)
        self.canvas.configure(width=cw,height=ch)
        self.canvas.update()
        # a mettre dans la fonction liée au bouton
        print(self.filename)
    def enregistrer(self):
        radical = os.path.splitext(self.filename)[0]
        nom_json = radical + ".json"
        with open(nom_json, "w") as fichier_json : 
            json.dump(self.objs, fichier_json, indent=4)

    def begin_rect(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        id = self.canvas.create_rectangle(
            x, y, x, y,outline='red', width = 2)
        self.current_rect = Rect.begin_with(id, x, y)
        print("Rect {} started at ({}, {})".format(id, x, y))

    def progress_rect(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.current_rect.update_end_with(x, y)
        self.canvas.coords(self.current_rect.id, *self.current_rect.get_coords())

    def end_rect(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        self.current_rect.update_end_with(x, y)
        self.canvas.coords(self.current_rect.id, *self.current_rect.get_coords())
        self.rects.append(self.current_rect)
        print("Rect {} ended at ({}, {})".format(self.current_rect.id, x, y))
        (x1, y1, x2, y2) = self.current_rect.get_coords()
        r_xg = min(x1, x2)
        r_xd = max(x1, x2)
        r_yh = min(y1, y2)
        r_yb = max(y1, y2)
        r_w = r_xd - r_xg
        r_h = r_yb - r_yh
        obj = {
            "x": int(r_xg * self.ratio),
            "y": int(r_yh * self.ratio),
            "width": int(r_w * self.ratio),
            "height": int(r_h * self.ratio),
        }
        self.objs.append(obj)
        print(obj)


        self.parent = tk.Tk()
    def additem():
        listbox.insert(tk.END, content.get())


    def deleteAll():
        listbox.delete(0, tk.END)


    def deleteselected():
        listbox.delete(tk.ANCHOR)


        content = tk.StringVar()
        entry = tk.Entry(self.parent, textvariable=content)
        entry.pack()

        button = tk.Button(self.parent, text="Add Item", command=additem)
        button.pack()

        button2 = tk.Button(self.parent, text="Delete list", command=deleteAll)
        button2.pack()

        button3 = tk.Button(self.parent, text="Delete selected", command=deleteselected)
        button3.pack()

        listbox = tk.Listbox(self.parent)
        listbox.pack


def main():
    root = tk.Tk()
    root.geometry("{}x{}".format(MAX_CANVAS_WIDTH, MAX_CANVAS_HEIGHT + 50))
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()