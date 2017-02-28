import gedcom
import parser
import datetime

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
                            return False

def divorceBeforeDeath_US06(allFamilies, allPersons):
    for i in range(len(allFamilies)):
        hubandID = allFamilies[i]['husband_id']
        wifeID = allFamilies[i]['wife_id']
        divorceDate = allFamilies[i]['divorce']

        for i in range (len(allPersons)):
            if((allPersons[i]['id'] == husbandID) or (allPersons[i]['id'] == wifeID)):
                if divorceDate is not None:
                    if allPersons[i]['alive'] is not True:
                        if allPersons[i]['deathdate'] < divorceDate:
                           print "For this Id Death before Divorce is not possible : " + husbandID + "  " + wifeID
                           return False
                        
#implemented user story 07
def ageLessThan150_US7(allPersons):
    for i in range(len(allPersons)):
        if allPersons[i]['age'] > 150:
            print "For ID "+allPersons[i]['id']+" Age gt 150 is not possible"
            return False

def birthAfterDeathOfParents_US_09(allPersons, allFamilies):
    for x in range(len(allFamilies)):
        children = []                                                                  # List to store the IDs for children if there are more than one children
        fatherID = allFamilies[x]['husband_id']                                        # Get Father's ID
        motherID = allFamilies[x]['wife_id']                                           # Get Mother's ID
        childTypeCheck = allFamilies[x]['child']                                       # If only One child then it contains ID's else for checking the type (List or None)
        if type(childTypeCheck) is None:                                               # If there are no child, No Error
            pass
        elif(type(childTypeCheck) is list):                                            # if there are multiple children
            for z in range(len(childTypeCheck)):
                currentChildID = childTypeCheck[z]                                     # Getting the id or current child
                for i in range(len(allPersons)):                                       # Looping throug all person dictionary to match the IDs and extract birth and date date
                    if(allPersons[i]['id'] == fatherID):
                        fatherDeathDate = allPersons[i]['deathdate']
                    if(allPersons[i]['id'] == motherID):
                        motherDeathDate = allPersons[i]['deathdate']
                    if(allPersons[i]['id'] == currentChildID):
                        childBirthDate = allPersons[i]['birthdate']

                        if(fatherDeathDate and motherDeathDate is not None):                        # If both parents have a death date
                            if(fatherDeathDate is not None and fatherDeathDate > childBirthDate):   # If father has a deathddate and its after the childbirth date
                                pass
                            else:
                                print "Father's Death date can't be before Child's Birth Date"
                            if(motherDeathDate is not None and motherDeathDate > childBirthDate):   # If mother has a deathdate and its after the childBirth Date
                                pass  
                            else:
                                print "Mother's Death date can't be before Child's Birth Date"
        else:                                                                           # If there is only one child, take childTypeCheck as ID
            for i in range(len(allPersons)):
                if(allPersons[i]['id'] == fatherID):                                    # Getting dates
                    fatherDeathDate = allPersons[i]['deathdate']
                if(allPersons[i]['id'] == motherID):
                    motherDeathDate = allPersons[i]['deathdate']
                if(allPersons[i]['id'] == childTypeCheck):
                    childBirthDate = allPersons[i]['birthdate']

                    if(fatherDeathDate and motherDeathDate is not None):                # Same check as above
                        if(fatherDeathDate is not None and fatherDeathDate > childBirthDate):
                            pass
                        else:
                            print "Father's Death date can't be before Child's Birth Date"
                        if(motherDeathDate is not None and motherDeathDate > childBirthDate):
                            pass  
                        else:
                            print "Mother's Death date can't be before Child's Birth Date"

                            
# user story 02 birth before marriage
def birthBeforeMarriage_US02(allFamilies, allPersons):
    for i in range(len(allFamilies)):
        husbandID = allFamilies[i]['husband_id']
        wifeID = allFamilies[i]['wife_id']
        birthDate = allPersons[i]['birthdate']
        marriageDate = allFamilies[i]['marriage']

        for i in range(len(allPersons)):
            if (allPersons[i]['id'] == husbandID) or (allPersons[i]['id'] == wifeID):
                if marriageDate is not None:
                    if birthDate > marriageDate:
                        print 'US02 violated - birth before marriage : ' + husbandID + '  ' + wifeID

# user story 03 birth before death
def birthBeforeDeath_US03 (allPersons):
    for i in range (len(allPersons)):
        personID = allPersons[i]['id']
        birthDate = allPersons[i]['birthdate']
        deathDate = allPersons[i]['deathdate']

        if deathDate is not None:
            if birthDate > deathDate:
                print "US03 violated - person died before birth : " + personID

# Implemented User Story 01
# Description: Dates (birth, marriage, divorce, death) should not be after the current date
today = datetime.datetime.now()
def datesBeforeCurrentDate_US01(allPersons,allFamilies):
    for i in range(len(allPersons)):
        if allPersons[i]['birthdate'] > today:
            print "For ID "+allPersons[i]['id']+ ' ' + "Birthdate is after the current date"
        if allPersons[i]['alive'] == "False":
            if allPersons[i]['deathdate'] > today:
                print "For ID "+allPersons[i]['id']+ ' ' + "Deathdate is after the current date"

    for i in range(len(allFamilies)):
        if allFamilies[i]['marriage'] != None:
            if allFamilies[i]['marriage'] > today:
                print "For ID "+allFamilies[i]['Family_id']+ ' ' + "Marriage is after the current date"
        if allFamilies[i]['divorce'] != None:
            if allFamilies[i]['divorce'] > today:
                print "For ID "+allFamilies[i]['Family_id']+ ' ' + "Divorce is after the current date"
    return False

# Implemented User Story 10
# Description: Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old

marriage_date = dict()
all_persons_dict = dict()

def marriageAfter14_US10(allPersons,allFamilies):
    all_persons_dict = {x['id']:x for x in allPersons}
    valid_marriage = dict()
    for family in allFamilies:
        husband_id = family['husband_id']
        wife_id = family['wife_id']
        marriage_date = family['marriage'].date() if family['marriage'] is not None else None
        if marriage_date is not None and husband_id is not None and wife_id is not None:
            husband_age = all_persons_dict[husband_id]['birthdate'].date()
            wife_age = all_persons_dict[wife_id]['birthdate'].date()
            if husband_age.year - marriage_date.year >= 14 and wife_age.year - marriage_date.year >= 14:
                valid_marriage[family['Family_id']] = True
            else:
                valid_marriage[family['Family_id']] = False
    return valid_marriage

                
if __name__ == '__main__':
    parsedData = gedcom.parse("sample.ged")     # Provide gedcom file path here
    fam = parser.forFamilies(parsedData)
    ind = parser.forIndividual(parsedData)

    marriageBeforeDeath_US05(fam,ind)
    ageLessThan150_US7(ind)
    birthBeforeDeath_US03 (ind)
    birthBeforeMarriage_US02(fam, ind)
    birthAfterDeathOfParents_US_09(fam, ind)
    divorceBeforeDeath_US06(fam, ind)
    datesBeforeCurrentDate_US01(ind,fam)    
    marriageAfter14_US10(ind,fam)