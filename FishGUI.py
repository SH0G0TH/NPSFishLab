from tkinter import *

root = Tk()

root.title("Test Test 123")

root.geometry("350x200")
lbl = Label(root, text="Tail?")
lbl.pack()


def onPress(event):
    lbl.config(text="Tail!")
    print("pressed")
def onRelease(event):
    lbl.config(text="Tailless")


btn = Button(root, text="???", fg = "red")
btn.bind("<ButtonPress-1>", onPress)
btn.bind("<ButtonRelease-1>", onRelease)


btn.pack()

root.mainloop()