#53a402f5-f9d1-410b-bd66-8237844f03f8
from chemspipy import ChemSpider

cs = ChemSpider('53a402f5-f9d1-410b-bd66-8237844f03f8')
searchString = str(raw_input("what would you like to search? "))
x =1
resultList = []

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

    cd = cs.get_compound(resultList[0].csid)
    print(cd.common_name)
    print(cd.molecular_weight)
    print(cd.molecular_formula)
