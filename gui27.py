import sys
from Tkinter import *
from PIL import Image, ImageTk
import urllib2

#calling of API
from chemspipy import ChemSpider
cs = ChemSpider('53a402f5-f9d1-410b-bd66-8237844f03f8')


# local variables to store data retrieved by queries
InitialDict = {}
CompoundDict = {}
formula = 'placeholder'
ReactantDict = {}

class popOut(Frame):
    def __init__(self,master):

        Frame.__init__(self,master)
        self.pack()

        self.top = Toplevel()
        self.top.geometry('800x500')
        self.create_secondWindow(self.top)

        self.mass = 0
        self.name
        self.ID
        self.mol_weight
        self.url

    def create_secondWindow(self,frame):
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

    def assignment(self):
        self.mass = amountNeeded.get()
        #self.create_another_widget(self.top)
        molar_amount = self.mass/self.mol_weight
        self.newLabel = Label(self.top, text=('You would like to make '+ str(molar_amount) +' mols of this compound'))
        self.newLabel.pack()
        self.synthesize['text']='Confirm amount'
        self.synthesize['command']=self.create_another_widget
        
    def create_another_widget(self):

        self.synthesize['text']  ='Calculate'
        self.synthesize['command'] = self.calculate
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

    def compileReactants(self):
        ReactantDict[self.finalEntry.get()]=self.var.get()

    def calculate(self):
        print(ReactantDict)
        for reactant in ReactantDict:
            ce = cs.search(reactant)
            anotherThing = self.mass/self.mol_weight
            aThing = float(ReactantDict[reactant])*anotherThing*ce[0].molecular_weight
            finalLabel = Label(self.top, text = 'You will need ' + str(aThing) + 'g of ' + reactant)
            finalLabel.pack()
        EndingLabel = Label(self.top, text = 'This is what you need to synthesize ' + str(self.mass) +'g of ' + self.name + ', now get to work!')
        EndingLabel.pack()
        
       
        

#the opening window of the applcation
class initialPage(Frame):
    def __init__(self,master):

        Frame.__init__(self,master)
        self.pack()

        self.Index = 0

        self.create_widgets()

    def create_widgets(self):
        self.newLabel = Label(self, text='Hello! Please enter what you would like to synthesize: ')
        self.newLabel.pack()

        self.Lb1 = Listbox(self,width=40,height=20)
        self.Lb1.pack(side=LEFT)
        self.Lb1.bind('<ButtonRelease-1>', self.get_list)

        
        self.compoundEntry = Entry(self,textvariable=mainCompound)
        self.compoundEntry.pack()

        self.compoundButton = Button(self,command=self.SearchBox,text= 'go!')
        self.compoundButton.pack()


        self.confirmLabel = Label(self)
        self.confirmLabel.pack(side=RIGHT)



    def SearchBox(self):
        string = mainCompound.get()
        cd = cs.search(string)
        for result in cd:
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
        #cf = cs.search(seltext)
        #GuiMass = cf[0].molecular_weight
        #GuiIndex = cf[0].csid
        #display the selected text
        mainIndex= InitialDict[seltext]
        CompoundDict[str(seltext)]=mainIndex
        oneMoreThing = cs.get_compound(mainIndex)
        self.confirmLabel['text'] = (seltext + ', ' + str(oneMoreThing.molecular_weight) + 'g/mol')
        self.newLabel['text'] = ('Please confirm that ' + seltext + ' is your choice')
        self.compoundButton['text'] = 'Confirm'
        self.compoundButton['command']=self.other_stuff

    def other_stuff(self):
        react = popOut(self)
    


root = Tk()
root.geometry('640x360')
root.title("Reagent Calculator")

mainCompound = StringVar(root)
amountNeeded = DoubleVar(root)

hello = initialPage(root)
root.mainloop()
