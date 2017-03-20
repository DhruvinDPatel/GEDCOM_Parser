import gedcom
import datetime
from prettytable import PrettyTable

today = datetime.datetime.now()
all_persons = []
all_families = []

def for_individuals(parsed_data):    
    individual = list(parsed_data.individuals)
    individual_table = PrettyTable()
    individual_table.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]

    for i in range(len(individual)):
        temp = individual[i]
        person = {}
        fname, lname = temp.name

        person['id'] = temp.id
        person['name'] = fname +" "+ lname
        person['gender'] = temp.gender
        person['birthdate'] = datetime.datetime.strptime(temp.birth.date, '%d %b %Y')
        birthDate = datetime.datetime.strptime(temp.birth.date,'%d %b %Y')

        if temp.__contains__('DEAT'):
            person['alive'] = False
            deathDate = (temp.__getitem__('DEAT')).date
            person['deathdate'] = datetime.datetime.strptime(deathDate, '%d %b %Y')
        else:
            person['deathdate'] = None
            person['alive'] = True

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
            person['spouses'] = None

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
            person['child'] = None

        dictlist = [person['id'],person['name'],person['gender'],person['birthdate'],person['age'],person['alive'],person['deathdate'],person['child'],person['spouses']]
        individual_table.add_row(dictlist)
        all_persons.append(person)
    print "Individuals"
    print(individual_table)
    return all_persons

def for_families(parsed_data):
    fa = list(parsed_data.families)
    family_table=PrettyTable()
    family_table.field_names = ["ID","Married","Divorced","Husband_ID","Husband Name", "Wife Id", "Wife Name", "Children"]

    for i in range(len(fa)):
        f = fa[i]
        family = {}
        family['Family_id'] = f.id
        #husband = f.partners[0]
        #wife = f.partners[1]
        if f.__contains__('DIV'):
            divorce = f.__getitem__('DIV').__getitem__('DATE').value
            family['divorce'] = datetime.datetime.strptime(divorce, '%d %b %Y')
        else:
            family['divorce'] = None
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
            family['child'] = None
        
        if f.__contains__('MARR'):
            md = (f.__getitem__('MARR')).date
            family['marriage'] = datetime.datetime.strptime(md, '%d %b %Y')
        else:
            family['marriage'] = None
        
        if f.__contains__('HUSB'):
            family['husband_id'] = f.__getitem__('HUSB').value
            family['husband_name'] = ' '.join(f.get_by_id(family['husband_id']).name)
        else:
            family['husband_id'] = None
            family['husband_name'] = None

        if f.__contains__('WIFE'):
            family['wife_id'] = f.__getitem__('WIFE').value
            family['wife_name'] = ' '.join(f.get_by_id(family['wife_id']).name)
        else:
            family['wife_id'] = None
            family['wife_name'] = None
        
        dictlist2 = [family['Family_id'],family['marriage'],family['divorce'],family['husband_id'],family['husband_name'],family['wife_id'],family['wife_name'],family['child']]
        family_table.add_row(dictlist2)
        all_families.append(family)
    print "Families"
    print(family_table)
    return all_families