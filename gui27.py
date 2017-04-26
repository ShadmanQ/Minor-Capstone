import sys
from Tkinter import *
from PIL import Image, ImageTk
import urllib2

#calling of API
from chemspipy import ChemSpider
cs = ChemSpider('53a402f5-f9d1-410b-bd66-8237844f03f8')


global theThing


def Searchbox():

    tempDict = {}
    
    string = compound.get()
    cd = cs.search(string)
    for result in cd:
        Lb1.insert(END,result.common_name)
        tempDict[result.common_name] = result.csid
    theThing = tempDict

    print(theThing)

def get_list(event):
    '''
    function to read the listbox selection
    and put the result in an entry widget
    '''

    #get selected line index
    index = Lb1.curselection()[0]
    #get the line's text in enterl
    seltext = Lb1.get(index)
    #display the selected text
    secondEntry['text'] = seltext
                

root = Tk()
compound = StringVar()
IDofInterest = 0;

root.geometry('854x480')
root.title("Reagent Calculator")
newLabel = Label(root, text='Hello! Please enter what you would like to synthesize: ').pack()

newEntry = Entry(root, textvariable=compound).pack()
newButt = Button(root,command = Searchbox,text = "Go!").pack()

Lb1 = Listbox(root,width=40,height=20)
Lb1.pack(side=LEFT)

secondEntry = Label(root,width=50)
secondEntry.pack()

Lb1.bind('<ButtonRelease-1>', get_list)

#interest = cs.get_compound(1679)
#
#theThing = interest.image_url
#photo = Image.open(urllib2.urlopen(theThing))
#photo = photo.resize((300, 300), Image.ANTIALIAS)
#display = ImageTk.PhotoImage(photo)

#PhotoLabel = Label(root, image=display)
#PhotoLabel.pack(side=LEFT)
root.mainloop()
