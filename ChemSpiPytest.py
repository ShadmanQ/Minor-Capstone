#53a402f5-f9d1-410b-bd66-8237844f03f8, security token to use API


#function protoype
def Seperate(dicto, theString):
    for i in range(0,len(theString)):
        if (i == len(theString)-1)&(theString[i].isupper() == True):
            dicto[str(theString[i])] = 1
            break
        if theString[i].isupper() == True:
            if theString[i+1].islower() == True:
                dicto[str(theString[i:i+2])] = 1
            else:
                dicto[str(theString[i])] = 1

    for i in range(0,len(dicto)):
        thingy = str(theString).find(dicto.keys()[i])
        interest = dicto.keys()[i]
        for j in range(thingy, len(theString)):
            if theString[j] == theString[len(theString)-1]:
                break
            if theString[j+2].isupper() == True | theString[j+1].isalpha() == True:
                dicto[interest] = 1
                break
            elif theString[j] == '{':
                for k in range(j,len(theString)):
                    if theString[k] == '}':
                        #print(int(cd.molecular_formula[j+1:k]))
                        num = int(theString[j+1:k])
                        dicto[interest]= num
                        break            
                break
                           

#calling of API
from chemspipy import ChemSpider
cs = ChemSpider('53a402f5-f9d1-410b-bd66-8237844f03f8')

#prompts user for compound of interest
searchString = str(raw_input("what would you like to search? "))

#iterator variable
x =1
#holds list of Compound objects
resultList = []

#note: result is a 'Compound' object, which is part of the ChemSpiPy wrapper
#not a string or int
for result in cs.search(searchString):
    print(str(x) + ". " + result.common_name)
    resultList.append(result)
    x+=1

if len(resultList) == 1:
    cd = cs.get_compound(resultList[0].csid)
    print(cd.molecular_weight)
    print(cd.molecular_formula)
    print(cd.image_url)


if len(resultList)> 1:
    print("Your search returned " + str(len(resultList)) + " results. Please specify which compound you are interested in")
    num = int(raw_input("Enter a number: "))

    cd = cs.get_compound(resultList[num-1].csid)
    print(cd.common_name)
    print(cd.molecular_weight)
    print(cd.molecular_formula)
    print(cd.image_url)


#initialization of an elements dictionary for the compound of interest
elements= {}

Seperate(elements, cd.molecular_formula)
print(elements)


amount = float(input("Please enter how much you much " + cd.common_name + " you would like to make in milligrams: "))

mol_amount = (amount/1000)/cd.molecular_weight

print("You would like to make " + str(amount) +" mg or  " + str("%.4f" % mol_amount) + " mols of this compound.")

react = str(raw_input("Please enter a reactant "))

rg = cs.search(react)
gf= cs.get_compound(rg[0].csid)

print(gf.common_name)
print(gf.monoisotopic_mass)
