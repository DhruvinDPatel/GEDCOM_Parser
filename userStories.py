import gedcom
import collections
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

		if(days <= 30 and days > 0):
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
	#print "ERROR: FAMILY: US10: Marriage after 14 Violated - For id "
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
				#print "".join(family['Family_id'])
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

def US23_unique_name_unique_dob(all_persons):
	name_birthdate_list = []
	for i in range(len(all_persons)):
		name = all_persons[i]['name']
		date_of_birth = str(all_persons[i]['birthdate'])
		temp = (name, date_of_birth)
		name_birthdate_list.append(temp)

	a = dict(Counter(name_birthdate_list))
	for k, v in a.iteritems():
		if v > 1:
			print "ERROR INDIVIDUAL: US23: Unique name Unique date_of_birth violated for: " + str(k)

def US25_unique_firstname_in_family(all_persons, all_families):
	family_child_name_birthdat = []
	name_birthdate_list = []
	
	for i in range(len(all_families)):
		child = all_families[i]['child']
		if child == None:
			return False
		else:
			for j in range(len(all_persons)):
				if all_persons[j]['id'] in child:
					name = all_persons[j]['name']
					date_of_birth = str(all_persons[j]['birthdate'])
					temp = (name, date_of_birth)
					name_birthdate_list.append(temp)
					
					a = dict(Counter(name_birthdate_list))
					for k, v in a.iteritems():
						if v > 1:
							print "ERROR INDIVIDUAL: US25: Unique first name in family: "+str(k)

# US36 - List recent deaths
# Description - List all people in a GEDCOM file who died in the last 30 days
def US36_Individual_died_within_last_30_days(all_persons):
	for person in all_persons:
		if person['alive'] != True:
			death_date = (person['deathdate'].date() - today.date())    
			if(death_date.days < 0 or  death_date.days < 30):    
				print "ERROR: INDIVIDUAL: US36: Died within last 30 days Violated. "+ person['id']
			return False
	return True

# US37 - List recent survivors
# Description - List all living spouses and descendants of people in a GEDCOM file who died in the last 30 days
def US37_Spouses_Descendants_died_within_last_30_days(all_persons,all_families):
	spouse_descendants = []
	died_within_last_30_days = []
	alive_descendats = []
	for person in all_persons:
		if person['alive'] != True:
			death_date = (person['deathdate'].date() - today.date())            
			if death_date.days < 0 : print "ERROR: Age cannot be LESS than 0"                        
			if death_date.days < 30:
				died_within_last_30_days.append(person['id'])
				
	for died in died_within_last_30_days:
		for family in all_families:
			if died in family['wife_id']:
				spouse_descendants.append(family['husband_id'])
				if family['child'] != None:                
					spouse_descendants.append(family['child'])
			if died in family['husband_id']:
				spouse_descendants.append(family['wife_id'])
				if family['child'] != None:                
					spouse_descendants.append(family['child'])
					
	for alive in spouse_descendants:
		for individual in all_persons:
			if alive == individual['id']:
				if individual['alive'] == True: 
					alive_descendats.append(individual['id'])
	
	print "US 37: List all living spouses and descendants of people in a GEDCOM file who died in the last 30 days are" + ' ' + ', '.join(alive_descendats)
	return alive_descendats

#US - 12 Parents not too old.
def US12_parents_not_too_old(all_persons, all_families):
	for i in range(len(all_families)):
		if all_families[i]['child'] != None:
			father_id = all_families[i]['husband_id']
			mother_id = all_families[i]['wife_id']
			child_id = all_families[i]['child']
			for x in range(len(all_persons)):
				if all_persons[x]['id'] == child_id:
					child_age = all_persons[x]['age']
				if all_persons[x]['id'] == father_id:
					father_age = all_persons[x]['age']
				if all_persons[x]['id'] == mother_id:
					mother_age = all_persons[x]['age']
					
					if ((father_age - child_age > 80) or (mother_age - child_age > 60)):
						print "ERROR: FAMILIES: US12: Parents too old violated. "  + child_id

def US32_multiple_births(all_persons):
	multilple_birth = set()
	for i  in range(len(all_persons)):
		for j in range(len(all_persons)):
			name = all_persons[i]['name']
			birthdate = all_persons[i]['birthdate']
			comp_date = all_persons[j]['birthdate']
			if all_persons[i]['id'] != all_persons[j]['id']:
				if(str(birthdate) == str(comp_date)):
					multilple_birth.add (name)
	print "\nUS32 Multilple Birth: " + "| ".join(str(x) for x in multilple_birth)
	return multilple_birth

def US28_order_siblings_by_age(all_persons, all_families):
	ordered_list = []
	for i in range(len(all_families)):
		if type(all_families[i]['child']) == list:
			children = all_families[i]['child']
			dictionary = {}
			for x in range(len(children)):
				id = children[x]
				for p in range(len(all_persons)):
					if(all_persons[p]['id'] == id):
						age = all_persons[p]['age']
						name = all_persons[p]['name']
						dictionary.update({name: age})
			s = sorted(dictionary.items(), key=lambda(k,v):(v,k), reverse=True)
			ordered_list.append(s)

	print "\nUS28: FAMILY: List of siblings in order of their age ".join(str(x) for x in ordered_list)
	return ordered_list

def US27_include_current_age(allPersons):
	print "US27 : Listing current age of individuals"
	for x in range(len(allPersons)):
		id = allPersons[x]['id']
		name = allPersons[x]['name']
		age = allPersons[x]['age']
		print name + "\t:" + id + "\t:" + str(age)
		
# US38 All living people with birthdays in the next 30 days
def US38_upcoming_birthdays(all_persons):
    today_m_d_parsed = datetime.datetime.strptime(today.strftime("%m-%d"),"%m-%d")  # used to remove year from full date
    for i in range(len(all_persons)):
        alive = all_persons[i]['alive']
        birthdate = all_persons[i]['birthdate']
        person = all_persons[i]['id']

        if alive == True:
            birthdate_object = datetime.datetime.strptime(birthdate.strftime("%m-%d"),"%m-%d")
            date_difference = birthdate_object - today_m_d_parsed
            if (date_difference <= datetime.timedelta(days=30) and date_difference > datetime.timedelta(days=0)) or (date_difference <=datetime.timedelta(days=365) and date_difference > datetime.timedelta(days=335)):
                print 'US38: Upcoming Birthday for person ID ' + str(person)
		
#US39 All living couples whose marriage anniversaries occur in the next 30 days
def US39_upcoming_anniversaries(all_persons, all_families):
    today_m_d_parsed = datetime.datetime.strptime(today.strftime("%m-%d"),"%m-%d")  # used to remove year from full date
    for i in range(len(all_families)):
        anniversary = all_families[i]['marriage']
        family_id = all_families[i]['Family_id']

        for x in range (len(all_persons)):
            alive = all_persons[x]['alive']

        if alive == True:
            if anniversary != None:
                    if all_persons[x]['alive'] == True:
                        anniversary_object = datetime.datetime.strptime(anniversary.strftime("%m-%d"), "%m-%d")
                        date_difference = anniversary_object - today_m_d_parsed
                        if (date_difference <= datetime.timedelta(days=30) and date_difference > datetime.timedelta(days=0)) or (
                                datetime.timedelta(days=365) >= date_difference > datetime.timedelta(days=335)):
                            print 'US39: Upcoming Anniversary for family ID' + str(family_id)

if __name__ == '__main__':
	parsed_data = gedcom.parse("sample.ged")     # Provide gedcom file path here
	fam = parser_gedcom.for_families(parsed_data)
	ind = parser_gedcom.for_individuals(parsed_data)

	recently_born = US35_people_born_recently(ind)
	print "US35 List of recently born:"
	print "| ".join(str(x) for x in recently_born)

	living_married = US30_list_living_married(fam, ind)
	print "\nUS30 List of people who are married and alive are as follows: "
	print "| ".join(str(x) for x in living_married)

	US05_marriage_before_death(fam,ind)
	US07_age_less_than_150(ind)
	US03_birth_before_death(ind)
	US02_birth_before_marriage(fam, ind)
	US09_birth_after_death_of_parents(fam, ind)
	US06_divorce_before_death(fam, ind)
	US01_dates_before_current_date(ind,fam)    
	
	valid_marriage = US10_marriage_after_14(ind,fam)
	print "ERROR: FAMILY: US10 Valid Marriage Violated for "
	print "| ".join(str(x) for x in valid_marriage.iterkeys())

	US15_fewer_than_fifteen_siblings(fam)
	US14_multiple_births_less_5(ind,fam)
	US16_male_last_name(ind)
	US21_correct_gender_for_role(fam,ind)
	US23_unique_name_unique_dob(ind)
	US25_unique_firstname_in_family(ind, fam)
	US36_Individual_died_within_last_30_days(ind)
	US32_multiple_births(ind)
	US37_Spouses_Descendants_died_within_last_30_days(ind,fam)
	US28_order_siblings_by_age(ind, fam)
	US27_include_current_age(ind)
	US38_upcoming_birthdays(ind)
	US39_upcoming_anniversaries(ind,fam)
