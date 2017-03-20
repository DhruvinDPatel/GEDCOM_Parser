import gedcom
import parser_gedcom
import datetime
from collections import Counter

today = datetime.datetime.now()

def US05_marriage_before_death(all_families, all_persons):
    for i in range(len(all_families)):
        husband_id = all_families[i]['husband_id']
        marriage_date = all_families[i]['marriage']
        wife_id = all_families[i]['wife_id']
        
        for i in range(len(all_persons)):
            if((all_persons[i]['id'] == husband_id) or (all_persons[i]['id'] == wife_id)):
                if marriage_date is not None:
                    if all_persons[i]['alive'] is not True:
                        if all_persons[i]['deathdate'] < marriage_date:
                            print "ERROR: FAMILY: US05: Marriage Before Death Violated: " + husband_id + "  " + wife_id
                            return False

def US06_divorce_before_death(all_families, all_persons):
    for i in range(len(all_families)):
        husband_id = all_families[i]['husband_id']
        wife_id = all_families[i]['wife_id']
        divorce_date = all_families[i]['divorce']

        for i in range (len(all_persons)):
            if((all_persons[i]['id'] == husband_id) or (all_persons[i]['id'] == wife_id)):
                if divorce_date is not None:
                    if all_persons[i]['alive'] is not True:
                        if all_persons[i]['deathdate'] < divorce_date:
                           print "ERROR: FAMILY: US06: Divorce Before Death Violated: " + husband_id + "  " + wife_id
                           return False
                        
#implemented user story 07
def US07_age_less_than_150(all_persons):
    for i in range(len(all_persons)):
        if all_persons[i]['age'] > 150:
            print "ERROR: INDIVIDUAL: US07: Age less than 150 Violated: For ID "+all_persons[i]['id']+" Age gt 150 is not possible"
            return False

def US09_birth_after_death_of_parents(all_families, all_persons):
    for x in range(len(all_families)):
        father_id = all_families[x]['husband_id']                                        # Get Father's ID
        mother_id = all_families[x]['wife_id']                                           # Get Mother's ID
        child_type_check = all_families[x]['child']  
        father_death_date = None
        mother_death_date = None                                     # If only One child then it contains ID's else for checking the type (List or None)
        if type(child_type_check) is None:                                               # If there are no child, No Error
            pass
        elif(type(child_type_check) is list):                                            # if there are multiple children
            for z in range(len(child_type_check)):
                current_child_id = child_type_check[z]                                                                          # Getting the id or current child
                for i in range(len(all_persons)):                                       # Looping throug all person dictionary to match the IDs and extract birth and date date
                    if(all_persons[i]['id'] == father_id):
                        father_death_date = all_persons[i]['deathdate']
                    if(all_persons[i]['id'] == mother_id):
                        mother_death_date = all_persons[i]['deathdate']
                    if(all_persons[i]['id'] == current_child_id):
                        child_birth_date = all_persons[i]['birthdate']

                        if(father_death_date and mother_death_date is not None):                        # If both parents have a death date
                            if(father_death_date is not None and father_death_date > child_birth_date):   # If father has a deathddate and its after the childbirth date
                                pass
                            else:
                                print "ERROR: FAMILY: US09: Violated- Father's (" + father_id + ") Death date can't be before Child's (" + current_child_id + ") Birth Date"
                                print "Father death Date: " + str(father_death_date)
                                print "Child Birth Date: " + str(child_birth_date)
                            if(mother_death_date is not None and mother_death_date > child_birth_date):   # If mother has a deathdate and its after the childBirth Date
                                pass  
                            else:
                                print "ERROR: FAMILY: US09: Violated- Mother's (" + mother_id + ") Death date can't be before Child's (" + current_child_id + ") Birth Date"
                                print "Mother death Date: " + str(mother_death_date)
                                print "Child Birth Date: " + str(child_birth_date)
        else:                                                                           # If there is only one child, take child_type_check as ID
            for i in range(len(all_persons)):
                if(all_persons[i]['id'] == father_id):                                    # Getting dates
                    father_death_date = all_persons[i]['deathdate']
                if(all_persons[i]['id'] == mother_id):
                    mother_death_date = all_persons[i]['deathdate']
                if(all_persons[i]['id'] == child_type_check):
                    child_birth_date = all_persons[i]['birthdate']

                    if(father_death_date and mother_death_date is not None):                # Same check as above
                        if(father_death_date is not None and father_death_date > child_birth_date):
                            pass
                        else:
                            print "ERROR: FAMILY: US09: Violated- Father's (" + father_id + ") Death date can't be before Child's (" + child_type_check + ") Birth Date"
                            print("Father death Date: " + str(father_death_date))
                            print("Child Birth Date: " + str(child_birth_date))
                        if(mother_death_date is not None and mother_death_date > child_birth_date):
                            pass  
                        else:
                            print "ERROR: FAMILY: US09: Violated- Mother's (" + mother_id + ") Death date can't be before Child's (" + child_type_check + ") Birth Date"
                            print("Mother death Date: " + str(mother_death_date))
                            print("Child Birth Date: " + str(child_birth_date))

#User story 30: List living married
def US30_list_living_married(all_families, all_persons):
    list_married_and_alive = set()
    for x in range(len(all_families)):
        husband_id = all_families[x]['husband_id']
        wife_id = all_families[x]['wife_id']

        
        for p in range(len(all_persons)):
            if(all_persons[p]['id'] == husband_id):
                if(all_persons[p]['alive'] == True):
                    name = all_persons[p]['name']
                    list_married_and_alive.add(name)                        

        for p in range(len(all_persons)):
            if(all_persons[p]['id'] == wife_id):
                if(all_persons[p]['alive'] == True):
                    name = all_persons[p]['name']
                    list_married_and_alive.add(name) 

    return list_married_and_alive   


# US35 List of people who were born recently

def US35_people_born_recently(all_persons):
    recently_born = []
    for i in range(len(all_persons)):
        bday = all_persons[i]['birthdate']
        days = int((today - bday).days)

        if(days == 30 or days < 30):
            recently_born.append(all_persons[i]['name'])

    return recently_born


# user story 02 birth before marriage
def US02_birth_before_marriage(all_families, all_persons):
    unique_id = set()
    for i in range(len(all_families)):
        husband_id = all_families[i]['husband_id']
        wife_id = all_families[i]['wife_id']
        marriage_date = all_families[i]['marriage']

        for x in range(len(all_persons)):
            if (all_persons[x]['id'] == husband_id): 
                birthdate = all_persons[x]['birthdate']
                if marriage_date is not None:
                    if birthdate > marriage_date:
                        unique_id.add(husband_id) 

            if (all_persons[x]['id'] == wife_id):
                birthdate = all_persons[x]['birthdate']
                if marriage_date is not None:
                    if birthdate > marriage_date:
                       unique_id.add(wife_id)

    print " ".join("ERROR: FAMILY: US02: Violated - Birth before Marriage - For ID: " + str(x) for x in unique_id)

# user story 03 birth before death
def US03_birth_before_death(all_persons):
    for i in range (len(all_persons)):
        person_id = all_persons[i]['id']
        birth_date = all_persons[i]['birthdate']
        death_date = all_persons[i]['deathdate']

        if death_date is not None:
            if birth_date > death_date:
                print "ERROR: INDIVIDUAL: US03: Birth Before Death Violated - Person with id "+ person_id+" died before birth" 

# Implemented User Story 01
# Description: Dates (birth, marriage, divorce, death) should not be after the current date
def US01_dates_before_current_date(all_persons,all_families):
    for i in range(len(all_persons)):
        if all_persons[i]['birthdate'] > today:
            print "ERROR: INDIVIDUAL: US01: Dates Before current date Violated - For ID "+all_persons[i]['id']+ ' ' + "Birthdate is after the current date"
        if all_persons[i]['alive'] == "False":
            if all_persons[i]['deathdate'] > today:
                print "ERROR: INDIVIDUAL: US01: Dates Before current date Violated - For ID "+all_persons[i]['id']+ ' ' + "Deathdate is after the current date"

    for i in range(len(all_families)):
        if all_families[i]['marriage'] != None:
            if all_families[i]['marriage'] > today:
                print "ERROR: INDIVIDUAL: US01: Dates Before current date Violated - For ID "+all_families[i]['Family_id']+ ' ' + "Marriage is after the current date"
        if all_families[i]['divorce'] != None:
            if all_families[i]['divorce'] > today:
                print "ERROR: INDIVIDUAL: US01: Dates Before current date Violated - For ID "+all_families[i]['Family_id']+ ' ' + "Divorce is after the current date"
    return False

# Implemented User Story 10
# Description: Marriage should be at least 14 years after birth of both spouses (parents must be at least 14 years old
marriage_date = dict()
all_persons_dict = dict()

def US10_marriage_after_14(all_persons,all_families):
    all_persons_dict = {x['id']:x for x in all_persons}
    valid_marriage = dict()
    for family in all_families:
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
                print "ERROR: FAMILY: US10: Marriage after 14 Violated - For id "+ family['Family_id']
    return valid_marriage

# Implemented User Story 14
# No more than five siblings should be born at the same time
def US14_multiple_births_less_5(all_persons,all_families):
    for family in all_families:
        if family['child'] != None:
            sibling_uids = family['child']
        siblings = list(x for x in all_persons if x['id'] in sibling_uids)
        sib_birthdays = []
        for sibling in siblings:
            sib_birthdays.append(sibling['birthdate'])
        result = Counter(sib_birthdays).most_common(1)
        for (a,b) in result:
            if b > 5:
                print "ERROR: FAMILY: US14: Less than 5 siblings born at once Violated - For id "+ family['Family_id']
                return False
    return True
    
# Implemented User Story 15
# There should be fewer than 15 siblings in a family
def US15_fewer_than_fifteen_siblings(all_families):
    for family in all_families:
        if family['child'] != None and len(family['child']) >= 15:
            print "ERROR: FAMILY: US15: Fewer than 15 siblings  Violated - For id "+ family['Family_id']
            return False
    return True

def US16_male_last_name(all_persons):
    last_name_set = set()
    for i in range(len(all_persons)):
        if all_persons[i]['gender'] == 'M':
            last_name_set.add(all_persons[i]['name'].split()[-1])
    if len(last_name_set) != 1:
        print "ERROR: INDIVIDUALS: US16: Male last name should be same - violated"

def US21_correct_gender_for_role(all_families,all_persons):
    for i in range(len(all_families)):
        husband_id = all_families[i]['husband_id']
        wife_id = all_families[i]['wife_id']

        for i in range(len(all_persons)):
            if all_persons[i]['id'] == husband_id:
                if all_persons[i]['gender'] == 'M':
                    continue    
                else:
                    print "ERROR: FAMILY: US 21: Correct gender for role is violated for husband_id: "+all_persons[i]['id']
            if all_persons[i]['id'] == wife_id:
                if all_persons[i]['gender'] == 'F':
                    continue
                else:
                    print "ERROR: FAMILY: US 21: Correct gender for role is violated for wife_id: "+all_persons[i]['id']


if __name__ == '__main__':
    parsed_data = gedcom.parse("sample.ged")     # Provide gedcom file path here
    fam = parser_gedcom.for_families(parsed_data)
    ind = parser_gedcom.for_individuals(parsed_data)

    print "US-35 Recently Born: "+ str(US35_people_born_recently(ind))
    
    living_married = US30_list_living_married(fam, ind)
    print "\nUS30 List of people who are married and alive are as follows: \n"
    print "\n".join(str(x) for x in living_married)

    US05_marriage_before_death(fam,ind)
    US07_age_less_than_150(ind)
    US03_birth_before_death(ind)
    US02_birth_before_marriage(fam, ind)
    US09_birth_after_death_of_parents(fam, ind)
    US06_divorce_before_death(fam, ind)
    US01_dates_before_current_date(ind,fam)    
    
    print "ERROR: FAMILY: US10 Valid Marriage Violated for " + str(US10_marriage_after_14(ind,fam))
    
    US15_fewer_than_fifteen_siblings(fam)
    US14_multiple_births_less_5(ind,fam)
    US16_male_last_name(ind)
    US21_correct_gender_for_role(fam,ind)