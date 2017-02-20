import gedcom
import datetime
from prettytable import PrettyTable

parsedData = gedcom.parse("sample.ged")
today = datetime.datetime.now()
allPersons = []
allFamilies = []

def forIndividual(parsedData):    
    individual = list(parsedData.individuals)
    individualTable = PrettyTable()
    individualTable.field_names = ["ID", "Name", "Gender", "Birthday", "Age", "Alive", "Death", "Child", "Spouse"]

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
            person['alive'] = None
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
        individualTable.add_row(dictlist)
        allPersons.append(person)
    print "Individuals"
    print(individualTable)
    return allPersons

def forFamilies(parsedData):
    fa = list(parsedData.families)
    familyTable=PrettyTable()
    familyTable.field_names = ["ID","Married","Divorced","Husband_ID","Husband Name", "Wife Id", "Wife Name", "Children"]

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
        familyTable.add_row(dictlist2)
        allFamilies.append(family)
    print "Families"
    print(familyTable)
    return allFamilies

<<<<<<< HEAD
def marriageBeforeDeath_US05(allFamilies, allPersons):
    for i in range(len(allFamilies)):
        husbandID = allFamilies[i]['husband_id']
        marriageDate = allFamilies[i]['marriage']
        wifeID = allFamilies[i]['wife_id']
        
        for i in range (len(allPersons)):
            if((allPersons[i]['id'] == husbandID) or (allPersons[i]['id'] == wifeID)):
                if marriageDate is not None:
                    if allPersons[i]['alive'] is not True:
                        if allPersons[i]['deathdate'] < marriageDate:
                            print "For this Id Death before Marriage is not possible : " + husbandID + "  " + wifeID
=======
#implemented user story 07
def ageLessThan150_US7(allPersons):
    for i in range(len(allPersons)):
        if allPersons[i]['age'] > 150:
            print "For ID "+allPersons[i]['id']+" Age gt 150 is not possible"
>>>>>>> 2c72a72093706bdc7c57d46df2880a640a8c0047
 
if __name__ == '__main__':
    parsedData = gedcom.parse("sample.ged")     # Provide gedcom file path here
    f = forFamilies(parsedData)
    ind = forIndividual(parsedData)
<<<<<<< HEAD
    marriageBeforeDeath_US05(f,ind)
=======
    ageLessThan150_US7(ind)
>>>>>>> 2c72a72093706bdc7c57d46df2880a640a8c0047
