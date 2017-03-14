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

formlength = len(cd.molecular_formula)
elements= []

for i in range(0,len(cd.molecular_formula)):
    if (i == len(cd.molecular_formula)-1)&(cd.molecular_formula[i].isupper() == True):
        print(cd.molecular_formula[i])
        break
    if cd.molecular_formula[i].isupper() == True:
        if cd.molecular_formula[i+1].isalpha() == True:
            print(cd.molecular_formula[i:i+2])
        else:
            print(cd.molecular_formula[i])
