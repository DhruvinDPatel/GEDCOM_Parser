import gedcom
import datetime
from prettytable import PrettyTable

parsed = gedcom.parse("sample.ged")     # Provide gedcom file path here
individual = list(parsed.individuals)
today = datetime.datetime.now()
individualTable = PrettyTable()
individualTable.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]
familyTable=PrettyTable()
familyTable.field_names = ["ID","Married","Divorced","Husband_ID","Husband Name", "Wife Id", "Wife Name", "Children"]
    
for i in range(len(individual)):
    temp = individual[i]
    person = {}
    fname, lname = temp.name

    person['id'] = temp.id
    person['name'] = fname +" "+ lname
    person['gender'] = temp.gender
    person['birthdate'] = temp.birth.date
    birthDate = datetime.datetime.strptime(temp.birth.date,'%d %b %Y')

    if temp.__contains__('DEAT'):
        person['alive'] = 'NA'
        deathDate = temp.__getitem__('DEAT')
        person['deathdate'] = deathDate.value
    else:
        person['deathdate'] = 'NA'
        person['alive'] = 'Y'

    if temp.__contains__('DEAT'):
        person['age'] = (datetime.datetime.strptime(temp.death.date,'%d %b %Y') - datetime.datetime.strptime(temp.birth.date,'%d %b %Y')).days/365
    else:
        person['age'] = (today - birthDate).days/365

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

    dictlist = [person['id'],person['name'],person['gender'],person['birthdate'],person['age'],person['alive'],person['deathdate'],person['child'],person['spouses']]
    individualTable.add_row(dictlist)

fa = list(parsed.families)
for i in range(len(fa)):
    f = fa[i]
    family = {}
    family['Family_id'] = f.id
    #husband = f.partners[0]
    #wife = f.partners[1]
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
        family['marriage'] = md
    else:
        family['marriage'] = 'NA'
    
    if f.__contains__('HUSB'):
        family['husband_id'] = f.__getitem__('HUSB').value
        family['husband_name'] = ' '.join(f.get_by_id(family['husband_id']).name)
    else:
        family['husband_id'] = 'NA'
        family['husband_name'] = 'NA'

    if f.__contains__('WIFE'):
        family['wife_id'] = f.__getitem__('WIFE').value
        family['wife_name'] = ' '.join(f.get_by_id(family['wife_id']).name)
    else:
        family['wife_id'] = 'NA'
        family['wife_name'] = 'NA'
    
    dictlist2 = [family['Family_id'],family['marriage'],family['divorce'],family['husband_id'],family['husband_name'],family['wife_id'],family['wife_name'],family['child']]
    familyTable.add_row(dictlist2)

print "Individuals"
print(individualTable)
print "Families"
print(familyTable)
