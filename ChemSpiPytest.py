#53a402f5-f9d1-410b-bd66-8237844f03f8, security token to use API


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
    print(cd.common_name)
    print(cd.molecular_weight)
    print(cd.molecular_formula)

if len(resultList)> 1:
    print("Your search returned " + str(len(resultList)) + " results. Please specify which compound you are interested in")
    num = int(raw_input("Enter a number: "))

    cd = cs.get_compound(resultList[num-1].csid)
    print(cd.common_name)
    print(cd.molecular_weight)
    print(cd.molecular_formula)


#initialization of an elements dictionary for the compound of interest
elements= {}

for i in range(0,len(cd.molecular_formula)):
    if (i == len(cd.molecular_formula)-1)&(cd.molecular_formula[i].isupper() == True):
        elements[str(cd.molecular_formula[i])] = 1
        break
    if cd.molecular_formula[i].isupper() == True:
        if cd.molecular_formula[i+1].islower() == True:
            elements[str(cd.molecular_formula[i:i+2])] = 1
        else:
            elements[str(cd.molecular_formula[i])] = 1

print(elements)

for i in range(0,len(elements)):
    thingy = str(cd.molecular_formula).find(elements.keys()[i])
    string = elements.keys()[i]
    for j in range(thingy, len(cd.molecular_formula)):
        if cd.molecular_formula[j+2].isupper
        if cd.molecular_formula[j] == '{':
            for k in range(j,len(cd.molecular_formula)):
                if cd.molecular_formula[k] == '}':
                    #print(int(cd.molecular_formula[j+1:k]))
                    num = int(cd.molecular_formula[j+1:k])
                    elements[string]= num
                    break
            
            break
                           
print(elements)
