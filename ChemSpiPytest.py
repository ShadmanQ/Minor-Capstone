from chemspipy import ChemSpider

cs = ChemSpider('53a402f5-f9d1-410b-bd66-8237844f03f8')
c = cs.get_compound(2157)
print(c.molecular_formula)
print(c.common_name)
print(c.molar_mass)
#53a402f5-f9d1-410b-bd66-8237844f03f8
#xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
