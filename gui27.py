from Tkinter import *

root = Tk()
newLabel = Label(root, text="Hello!")
newLabel.pack(side=LEFT)
newEntry = Entry(root, bd =5)
newEntry.pack(side =LEFT)
newButt = Button(root, text = "Go!")
newButt.pack(side=RIGHT)
root.mainloop()
