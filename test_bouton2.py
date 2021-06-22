from tkinter import *
from tkinter.filedialog import askopenfilename


def calcul ():
    filename = askopenfilename()  # a mettre dans la fonction liée au bouton
    print(filename)


MyWindow = Tk()

MyWindow.title("trouver une arme")
MyWindow.geometry("300x200")


ButtonCalcul = Button(MyWindow, text ="Calculer", command = calcul)
ButtonCalcul.grid(row=1,column=0, padx = 5, pady = 50)



MyWindow.mainloop()