import tkinter as tk

from model import *

RECT_BORDER_COLOR = "#4eccde"

class App(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.current_rect = None
        self.rects = []
        self.init_widgets()
        
    def init_widgets(self):
        self.canvas = tk.Canvas(
            self.parent, width=800, height=400, bg="white")
        self.canvas.grid(row=0, column=0, sticky="nsew")
        self.canvas.bind("<Button-1>", self.begin_rect)
        self.canvas.bind("<ButtonRelease-1>", self.end_rect)
        self.canvas.bind("<B1-Motion>", self.progress_rect)

    def begin_rect(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        id = self.canvas.create_rectangle(
            x, y, x, y, fill=RECT_BORDER_COLOR)
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
        self.current_rect = None

def main():
    root = tk.Tk()
    root.geometry("900x500")
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
