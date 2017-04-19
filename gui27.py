import sys
from Tkinter import *
from PIL import Image, ImageTk
import urllib2

#calling of API
from chemspipy import ChemSpider
cs = ChemSpider('53a402f5-f9d1-410b-bd66-8237844f03f8')


def testfunction():
    x =1
    string = comp.get()
    cd = cs.search(string)
    for result in cd:
        newString = (str(x) + ' ' + result.common_name)
        mLabel2 = Label(root,text=newString).pack()
        x+=1

root = Tk()
comp = StringVar()

root.geometry('1280x720')
root.title("Reagent Calculator")
newLabel = Label(root, text='Hello! Please enter what you would like to synthesize: ').pack()

newButt = Button(root,command = testfunction,text = "Go!").pack()

newEntry = Entry(root, textvariable=comp).pack()
Lb1 = Listbox(root)
Lb1.pack()


interest = cs.get_compound(1679)

theThing = interest.image_url
photo = Image.open(urllib2.urlopen(theThing))
photo = photo.resize((300, 300), Image.ANTIALIAS)
display = ImageTk.PhotoImage(photo)

PhotoLabel = Label(root, image=display)
PhotoLabel.pack(side=LEFT)


root.mainloop()
