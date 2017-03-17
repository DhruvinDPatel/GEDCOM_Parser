import unittest
import parser
import gedcom
import datetime
import HTMLTestRunner

# In[]

parsedData = gedcom.parse("sample.ged")
fam = parser.forFamilies(parsedData)
ind = parser.forIndividual(parsedData)

# In[]:
#Implemnted test cases for user story 07
class TestMarriageBeforeDeath_US05(unittest.TestCase):
    def test_marriageBeforeDeath_US05_marriage_availibility(self):
        self.assertIsNotNone(fam[0]['marriage'], "ERROR: Family: US05: Marriage " + str(fam[0]['marriage']) + " Marriage Date cannot be None.")

    def test_marriageBeforeDeath_US05_MarriageDateType(self):
        self.assertEqual(type(fam[0]['marriage']), datetime.datetime, "ERROR: Family: US07: Marriage date " + str(fam[0]['marriage']) + " Marriage date is of wrong type.")

    def test_marriageBeforeDeath_US05_ReturnsFalse(self):
        self.assertFalse(parser.marriageBeforeDeath_US05(fam, ind), "ERROR: Family: US05: Returns False Function can't return False.")

    def test_marriageBeforeDeath_US05_ageIsString(self):
        self.assertNotEquals(type(ind[0]['age']), str, "ERROR: Individual: US07: Age " + str(ind[0]['age']) + " Age can't be float.")

    def test_marriageBeforeDeath_US05_ReturnsNone(self):
        self.assertIsNone(parser.marriageBeforeDeath_US05(fam, ind), "ERROR: Family: US05: Returns None Function can't return None.")

#Implemnted test cases for user story 07
class TestAgeLessThan150_US7(unittest.TestCase):
    def test_ageLessThan150_US7_ageIsNone(self):
        self.assertIsNotNone(ind[0]['age'], "ERROR: Individual: US07: Age " + str(ind[0]['age']) + " Age cannot be None.")

    def test_ageLessThan150_US7_isInteger(self):
        self.assertEqual(type(ind[0]['age']),int, "ERROR: Individual: US07: Age " + str(ind[0]['age']) + "Age is not an Integer.")

    def test_ageLessThan150_US7_ageIsNegative(self):
        self.assertGreater(ind[0]['age'], 0, "ERROR: Individual: US07: Age " + str(ind[0]['age']) + " Age can't be negative.")

    def test_ageLessThan150_US7_ageIsFloat(self):
        self.assertNotEquals(type(ind[0]['age']), float, "ERROR: Individual: US07: Age " + str(ind[0]['age']) + " Age can't be float.")

    def test_ageLessThan150_US7_ReturnsFalse(self):
        self.assertFalse(parser.ageLessThan150_US7(ind), "ERROR: Individual: US07: Returns False, Function can't return False.")

# Reporting
test_classes_to_run = [TestMarriageBeforeDeath_US05, TestAgeLessThan150_US7] # Include test cases here 
loader = unittest.TestLoader() 
suites_list = []
for test_class in test_classes_to_run:
    suite = loader.loadTestsFromTestCase(test_class)
    suites_list.append(suite)
big_suite = unittest.TestSuite(suites_list)
runner = unittest.TextTestRunner(verbosity=2).run(big_suite)
outfile = open("Report.html", "w")
runner = HTMLTestRunner.HTMLTestRunner(
                stream=outfile,
                title='User Stories UnitTest Report',
                description='This demonstrates the report output by ssw555BB2017Spring Team'
                )

runner.run(big_suite)
outfile.close()