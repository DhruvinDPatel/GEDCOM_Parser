import gedcom
import datetime
from prettytable import PrettyTable

#gedcomfile = gedcom.parse("sample.ged")
parsed = gedcom.parse("sample.ged")
individual = list(parsed.individuals)
today = datetime.datetime.now()
x = PrettyTable()
x.field_names = ["Child", "Name", "Gender", "Age", "Alive", "Birthday", "Spouse", "Death", "ID"]
y=PrettyTable()
y.field_names = ["Wife_ID", "Husband_ID", "Divorce", "Wife Name", "Family Id", "Marriage", "Husband Name", "Child"]
    
for i in range(len(individual)):
    temp = individual[i]
    person = {}
    fname, lname = temp.name

    person['id'] = temp.id
    person['name'] = fname +" "+ lname
    person['gender'] = temp.gender
    #person['tag'] = temp.tag
    person['birthdate'] = temp.birth.date
    bd = datetime.datetime.strptime(temp.birth.date,'%d %b %Y')

    if temp.__contains__('DEAT'):
        person['alive'] = 'NA'
        dd = temp.__getitem__('DEAT')
        person['deathdate'] = dd.value
    else:
        person['deathdate'] = 'NA'
        person['alive'] = 'Y'

    if temp.__contains__('DEAT'):
        person['age'] = (datetime.datetime.strptime(temp.death.date,'%d %b %Y') - datetime.datetime.strptime(temp.birth.date,'%d %b %Y')).days/365
    else:
        person['age'] = (today - bd).days/365

    if temp.__contains__('FAMS'):
        spouses = temp.__getitem__('FAMS')
        if isinstance(spouses, gedcom.Element):
            person['spouses'] = spouses.value
        else:
            spouses_id = []
            for i in range(len(spouses)):
                spouses_id.insert(i,spouses[i].value)
            person['spouses'] = spouses_id
    else:
        person['spouses'] = 'NA'

    if temp.__contains__('FAMC'):
        child = temp.__getitem__('FAMC')
        if isinstance(child, gedcom.Element):
            person['child'] = child.value
        else:
            child_id = []
            for i in range(len(child)):
                child_id.append(child[i].value)
            person['child'] = child_id
    else:
        person['child'] = 'NA'

    #print temp
    b = person.values()
    #print(b)
    x.add_row(b)
    #print person
    #print temp.child_elements
    #print "_____________"
    #print temp
    #print dir(temp)

fa = list(parsed.families)
for i in range(len(fa)):
    f = fa[i]
    family = {}
    family['Family_id'] = f.id
    #husband = f.partners[0]
    #wife = f.partners[1]
    #marriage = f.get_list('MARR')[0], .child_elements.__getitem__('DATE')
    if f.__contains__('DIV'):
        divorce = f.__getitem__('DIV').__getitem__('DATE').value
        family['divorce'] = divorce
    else:
        family['divorce'] = 'NA'
    #no_of_children = len(children)

    if f.__contains__('CHIL'):
        child = f.__getitem__('CHIL')
        if isinstance(child, gedcom.Element):
            family['child'] = child.value
        else:
            child_id = []
            for i in range(len(child)):
                child_id.append(child[i].value)
            family['child'] = child_id
    else:
        family['child'] = 'NA'
    
    if f.__contains__('MARR'):
        md = (f.__getitem__('MARR')).date
        #print md
    else:
        family['marriage'] = 'NA'

    family['husband_id'] = f.partners[0].value
    family['husband_name'] = ' '.join(f.get_by_id(f.partners[0].value).name)
    family['wife_id'] = f.partners[1].value
    family['wife_name'] = ' '.join(f.get_by_id(f.partners[1].value).name)
    family['marriage'] = md

    #print family
    c = family.values()
    #print(c)
    y.add_row(c)
    #print family
    #print dir(f)
    #print f.get_list
    #print dir(husband)
    #print dir(wife)
    #print dir(divorce)
    #print type(marriage)

print(x)
print(y)
