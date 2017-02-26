from chemspipy import ChemSpider

cs = ChemSpider('53a402f5-f9d1-410b-bd66-8237844f03f8')
c = cs.get_compound(2157)
print(c.molecular_formula)
print(c.common_name)
print(str(c.molecular_weight) + ' g/mol')
print(c.spectra)
#53a402f5-f9d1-410b-bd66-8237844f03f8
#xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
for result in cs.search('LSD'):
    print(result.csid)
    thing = result.csid

d = cs.get_compound(thing)
print(d.common_name)
