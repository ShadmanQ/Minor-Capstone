# -*- coding: cp1252 -*-

#importing requisite libraries
import sys
import io
from Tkinter import *
from PIL import Image, ImageTk
from urllib2 import urlopen
import requests
from bs4 import BeautifulSoup

#calling of API
from chemspipy import ChemSpider
cs = ChemSpider('53a402f5-f9d1-410b-bd66-8237844f03f8')


# local variables to store data retrieved by queries
InitialDict = {}
CompoundDict = {}
formula = 'placeholder'
ReactantDict = {}
ChemData = []
  
#the first window of this application
class initialPage(Frame):
    def __init__(self,master):

        Frame.__init__(self,master)
        self.pack()

        self.Index = 0

        self.create_widgets()

    def create_widgets(self):
        #prompt which asks for a compound
        self.introLabel = Label(self, text="Hello! Please enter the compound you'd like to learn about")
        self.introLabel.pack()

        #listbox object which stores the query results
        self.Lb1 = Listbox(self,width=20,height=12)
        self.Lb1.pack(side=LEFT)
        self.Lb1.bind('<ButtonRelease-1>', self.get_list)

        
        self.compoundEntry = Entry(self,textvariable=mainCompound)
        self.compoundEntry.pack()

        self.compoundButton = Button(self,command=self.SearchBox,text= 'Search!')
        self.compoundButton.pack()

        self.confirmLabel = Label(self)
        self.confirmLabel.pack(side=RIGHT)

        self.propButton= Button(self)

        self.synthButton = Button(self)

        self.spectraButton = Button(self)
        
    #function which accesses the ChemSpider API and retrieves
    def SearchBox(self):
        string = mainCompound.get()
        searchResults = cs.search(string)
        for result in searchResults:
            self.Lb1.insert('end',result.common_name)
            InitialDict[str(result.common_name)]=result.csid
        

    def get_list(self,confirmLabel):
        '''
        function to read the listbox selection
        and put the result in an entry widget
        '''

        #get selected line index
        index = self.Lb1.curselection()[0]
        #get the line's text in enterl
        seltext = self.Lb1.get(index)
        #display the selected text
        mainIndex= InitialDict[seltext]
        CompoundDict[str(seltext)]=mainIndex
        oneMoreThing = cs.get_compound(mainIndex)
        #self.confirmLabel['text'] = (seltext + ', ' + str(oneMoreThing.molecular_weight) + 'g/mol')
        self.introLabel['text'] = ('What would you like to learn about ' + seltext + '?')
        self.Index = InitialDict[seltext]
        self.propButton['text']=('Properties')
        self.propButton['command']=self.properties
        self.propButton.pack(anchor=W)
        self.synthButton['text'] = 'Synthesis Help'
        self.synthButton['command'] = self.synth
        self.synthButton.pack(anchor=W)
        self.spectraButton['text'] = 'Obtain Spectra'
        self.spectraButton['command'] = self.spectra
        self.spectraButton.pack(anchor=W)
        #self.compoundButton['command']=self.other_stuff

    def synth(self):
        react = synthWindow(self)

    def properties(self):
        prop = propertyWindow(self,self.Index)

    def spectra(self):
        spect = spectraWindow(self,self.Index)

class spectraWindow(Frame):
    def __init__(self,master,number):
        Frame.__init__(self,master)
        self.pack()
        
        self.index = number
        self.top = Toplevel()
        self.top.geometry('640x300')
        self.top.title("Spectra")

        self.create_spectraWindow(self.top)

    def create_spectraWindow(self,frame):
        rawSpectraList = cs.get_compound(self.index).spectra
        if (len(rawSpectraList) <1):
            noSpectraLabel = Label(frame, text='Unfortunately, there do not seem to be any spectra available for this compound.')
            noSpectraLabel.pack()

class propertyWindow(Frame):
    def __init__(self,master,number):
        Frame.__init__(self,master)
        self.pack()

        self.index = number
        self.meltMessage = 'Data for this is unavailable'
        self.boilMessage = 'Data for this is unavailable'
        self.appMessage = 'Data for this is unavailable'
        self.safeMessage = 'Data for this is unavailable'

        self.top = Toplevel()
        self.top.geometry('640x300')
        self.top.title("Properties of your compound")
        self.url = str("http://www.chemspider.com/Chemical-Structure." + str(self.index) + ".html")

        self.create_propertyWindow(self.top)
        
        
    def create_propertyWindow(self,frame):

        propertyRetrieval = cs.get_compound(self.index)

        print(propertyRetrieval.molecular_formula)
        
        r = requests.get(self.url)
        soup = BeautifulSoup(r.content, "html.parser")
        f_data = soup.find_all("ul")

        for x in range(0,len(f_data)):
            ChemData.append((f_data[x].text)) 

        for x in range(0,len(ChemData)):
            if "Melting Point" in ChemData[x]:
                meltsearch = ChemData[x]
                s1 = (meltsearch.find("Melting Point"))
                s2 = len("Melting Point")
                s3 = s1+s2
                for i in range(s3,len(meltsearch)):
                    if meltsearch[i] == 'C':
                        self.meltMessage=(meltsearch[i-5:i+1])
                        break
                break

        for x in range(0,len(ChemData)):
            if "Experimental Boiling Point" in ChemData[x]:
               boilsearch = ChemData[x]
               s1 = (boilsearch.find("Experimental Boiling Point"))
               s2 = len("Experimental Boiling Point")
               s3=s1+s2
               for i in range(s3,len(boilsearch)):
                    if boilsearch[i] == 'C':
                        self.boilMessage=(boilsearch[i-5:i+1])
                        break
               break
            
        for x in range(0,len(ChemData)):
            if "Appearance" in ChemData[x]:
                boilsearch = ChemData[x]
                s1 = (boilsearch.find("Appearance"))
                s2 = len("Appearance")
                s3=s1+s2
                print(boilsearch[s3])
                for i in range(s3,len(boilsearch)):
                    if ((boilsearch[i] == '.') or ((boilsearch[i] == 'O') and boilsearch[s3+4] != 'O')):
                        self.appMessage =(boilsearch[s3+4:i])
                        print(self.appMessage)
                        break
                break
                
        self.molLabel = Label(frame, text=propertyRetrieval.common_name, font = "Calibri 16 bold")
        self.molLabel.grid(row=0,sticky=W)
        self.top.grid_rowconfigure(1,minsize=15)

        self.formLabel = Label(frame, text='Molecular Formula:')
        self.formLabel.grid(row=2,sticky=W)
        self.top.grid_rowconfigure(3,minsize=15)
        
        self.massLabel = Label(frame, text='Molecular Mass:')
        self.massLabel.grid(row = 4,sticky=W)
        self.top.grid_rowconfigure(5,minsize=15)

        self.meltLabel = Label(frame, text='Melting Point ')
        self.meltLabel.grid(row=6,sticky=W)
        self.top.grid_rowconfigure(7,minsize=15)
        
        self.boilLabel = Label(frame, text='Boiling Point:')
        self.boilLabel.grid(row=8,sticky=W)
        self.top.grid_rowconfigure(9,minsize=15)

        self.appLabel = Label(frame, text='Appearance:')
        self.appLabel.grid(row=10,sticky=W)
        self.top.grid_rowconfigure(11,minsize=15)

        self.formText = Label(frame, text = propertyRetrieval.molecular_formula).grid(row=2, column=1)

        self.massText = Label(frame, text = (str(propertyRetrieval.molecular_weight)+' g/mol')).grid(row=4,column=1)

        self.meltText = Label(frame, text = self.meltMessage).grid(row=6,column=1)

        self.boilText = Label(frame, text=self.boilMessage).grid(row=8,column=1)
        
        self.appText = Label(frame, text=self.appMessage).grid(row=10,column=1)

class synthWindow(Frame):
    def __init__(self,master):

        Frame.__init__(self,master)
        self.pack()

        self.top = Toplevel()
        self.top.geometry('800x500')
        self.create_synthWindow(self.top)

        self.mass = 0
        self.name
        self.ID
        self.mol_weight
        self.url

    def create_synthWindow(self,frame):
        for compound in CompoundDict:
            self.name = compound
            self.ID = CompoundDict[compound]

        self.popLabel = Label(frame, text =('Please enter the amount of ' + self.name + ' you would like to make in grams'))
        self.popLabel.pack(side=TOP,anchor=W)

        self.amount = Entry(frame,textvariable=amountNeeded)
        self.amount.pack(side=TOP,anchor=W)

        self.synthesize = Button(frame, text='Enter',command = self.assignment)
        self.synthesize.pack(side=TOP,anchor=W)

        cf = cs.get_compound(self.ID)
        self.mol_weight =cf.molecular_weight
        self.url = cf.image_url
        

        self.imageBytes = urlopen(self.url).read()
        self.data_stream = io.BytesIO(self.imageBytes)

        self.pil_image = Image.open(self.data_stream)
        self.pil_image = self.pil_image.resize((250,250),Image.ANTIALIAS)
        
        self.photo = ImageTk.PhotoImage(self.pil_image)
        panel = Label(self.top, image = self.photo)
        panel.pack(side=BOTTOM, anchor = E)
 
    def assignment(self):
        self.mass = amountNeeded.get()
        molar_amount = self.mass/self.mol_weight
        self.newLabel = Label(self.top, text=('You would like to make '+ str(molar_amount) +' mols of this compound'))
        self.newLabel.pack()
        self.synthesize['text']='Confirm amount'
        self.synthesize['command']=self.create_another_widget
        
    def create_another_widget(self):

        self.var = StringVar()
        self.var.set('#')

        self.dropDown = OptionMenu(self.top, self.var, '1','2','3','4','5','6','7','8','9','10')
        self.dropDown.pack(side=LEFT)

        self.finalEntry = Entry(self.top)
        self.finalEntry.pack(side=LEFT)

        self.finalButton = Button(self.top)
        self.finalButton['text'] = 'Add reactant'
        self.finalButton['command'] = self.compileReactants
        self.finalButton.pack(side=LEFT)

        self.synthButton = Button(self.top)
        self.synthButton['text']='Calculate'
        self.synthButton['command']=self.calculate
        self.synthButton.pack(side=LEFT,anchor=S)
        

    def compileReactants(self):
        ReactantDict[self.finalEntry.get()]=self.var.get()

    def calculate(self):
        print(ReactantDict)
        for reactant in ReactantDict:
            ce = cs.search(reactant)
            anotherThing = self.mass/self.mol_weight
            aThing = float(ReactantDict[reactant])*anotherThing*ce[0].molecular_weight
            finalLabel = Label(self.top, text = 'You will need ' + str(aThing) + 'g of ' + reactant)
            finalLabel.pack(anchor=E)
        EndingLabel = Label(self.top, text = 'This is what you need to synthesize ' + str(self.mass) +'g of ' + self.name + ', now get to work!')
        EndingLabel.pack(anchor=E)
root = Tk()
root.geometry('580x300')
root.title("Reagent Calculator")

mainCompound = StringVar(root)
amountNeeded = DoubleVar(root)

hello = initialPage(root)
root.mainloop()
