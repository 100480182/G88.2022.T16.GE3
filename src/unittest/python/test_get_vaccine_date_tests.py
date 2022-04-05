import json
import unittest
from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException
from uc3m_care import VaccinationAppoinment
from test_utils import TestUtils


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)  # add assertion here

    @classmethod
    def setUpClass(cls) -> None:
        # CREATE THE FOLDERS AND FILES FOR TESTING
        # setUpClass JUST AFTER THE OBJECT HAS BEEN CREATED
        TestUtils.setup_folders()

    @classmethod
    def tearDownClass(cls) -> None:
        # DELETE THE JSON FILES AT THE END OF THE TEST PROCESS
        # IF YOU WANT TO SEE THE CONTENT OF THE FILES
        # PLEASE COMMENT THE SENTENCE BELOW
        # AND AT THE END OF THE TESTS YOU CAN TAKE A LOOK AT THE CONTENT
        # tearDownClass IS EXECUTED AT THE END OF THE PROCESS
        # TestUtils.cleanup_all_folders()
        pass

    def setUp(self) -> None:
        """setUp IS EXECUTED ONCE BEFORE EACH TEST"""
        self.patient_id = "e19cca80-bb93-42aa-ab0f-780b0caa7d46"
        self.registration_type = "REGULAR"
        self.name_surname = "JOSE LOPEZ"
        self.phone_number = "+34123456789"
        self.age = 21

    def test_vaccine_date_valid(self):
        """testing when the json file is valid and error free"""
        my_manager = VaccineManager()
        my_manager.request_vaccination_id(patient_id=self.patient_id,
                                          registration_type=self.registration_type,
                                          name_surname=self.name_surname,
                                          phone_number=self.phone_number,
                                          age=self.age)
        test_file = "valid.json"
        res = my_manager.get_vaccine_date(test_file)

        try:
            with open(my_manager.vaccination_appointments, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
                found = False
                for appointment in data:
                    if res == appointment["_VaccinationAppoinment__vaccination_signature"]:
                        found = True
                        break
                if not found:
                    self.assertEqual(False, True)
        except FileNotFoundError:
            self.assertEqual(False, True)

        self.assertEqual(res, "cb2cf35dfe5417908aea0f9b2fde1b7622069a6bf58a10e9c25241a8a738de3c")

    def test_vaccine_date_node1_delete(self):
        """testing when node 1 (File) is deleted"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node1_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node1_duplicate(self):
        """testing when node 1 (File) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node1_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node2_delete(self):
        """testing when node 2 (Begin_object) is deleted"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node2_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node2_duplicate(self):
        """testing when node 2 (Begin_object) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node2_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node3_delete(self):
        """testing when node 3 (Data) is deleted"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node3_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request empty", cm.exception.message)

    def test_vaccine_date_node3_duplicate(self):
        """testing when node 3 (Data) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node3_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node4_delete(self):
        """testing when node 4 (End_object) is deleted"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node4_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node4_duplicate(self):
        """testing when node 4 (End_object) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node4_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node5_modify(self):
        """testing when node 5 ('{') is modified"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node5_modify.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node6_delete(self):
        """testing when node 6 (Field1) is deleted"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node6_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node6_duplicate(self):
        """testing when node 6 (Field1) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node6_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node7_delete(self):
        """testing when node 7 (Seperator) is deleted"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node7_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node7_duplicate(self):
        """testing when node 7 (Seperator) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node7_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node8_delete(self):
        """testing when node 8 (Field2) is deleted"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node8_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node8_duplicate(self):
        """testing when node 8 (Field2) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node8_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node9_modify(self):
        """testing when node 9 ('}') is modified"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node5_modify.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node10_delete(self):
        """testing when node 10 (Label_Field1) is deleted"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node10_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node10_duplicate(self):
        """testing when node 10 (Label_Field1) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node10_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node11_delete(self):
        """testing when node 11 (Equals) is deleted"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node11_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node11_duplicate(self):
        """testing when node 11 (Equals) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node11_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node12_delete(self):
        """testing when node 12 (Value_Field1) is deleted"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node12_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node12_duplicate(self):
        """testing when node 12 (Value_Field1) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node12_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node13_modify(self):
        """testing when node 13 (',') is modified"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node13_modify.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node14_delete(self):
        """testing when node 14 (Label_Field2) is deleted"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node14_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node14_duplicate(self):
        """testing when node 14 (Label_Field2) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node14_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node15_delete(self):
        """testing when node 15 (Equals) is deleted"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node15_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node15_duplicate(self):
        """testing when node 15 (Equals) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node15_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node16_delete(self):
        """testing when node 16 (Value_Field2) is deleted"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node16_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node16_duplicate(self):
        """testing when node 16 (Value_Field2) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node16_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node17_delete(self):
        """testing when node 17 (Quote) is deleted"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node17_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node17_duplicate(self):
        """testing when node 17 (Quote) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node17_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node18_delete(self):
        """testing when node 18 (Value_Label1) is deleted"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node18_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("PatientSystemID key missing", cm.exception.message)

    def test_vaccine_date_node18_duplicate(self):
        """testing when node 18 (Value_Label1) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node18_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("PatientSystemID key missing", cm.exception.message)

    def test_vaccine_date_node19_delete(self):
        """testing when node 19 (Quote) is deleted"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node19_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node19_duplicate(self):
        """testing when node 19 (Quote) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node19_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node20_modify(self):
        """testing when node 20 (':') is modified"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node20_modify.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node21_delete(self):
        """testing when node 21 (Quote) is deleted"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node21_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node21_duplicate(self):
        """testing when node 21 (Quote) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node21_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node22_delete(self):
        """testing when node 22 (Valuel1) is deleted"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node22_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("SystemID must be 32 characters long", cm.exception.message)

    def test_vaccine_date_node22_duplicate(self):
        """testing when node 22 (Valuel1) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node22_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("SystemID must be 32 characters long", cm.exception.message)

    def test_vaccine_date_node23_delete(self):
        """testing when node 23 (Quote) is deleted"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node23_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node23_duplicate(self):
        """testing when node 23 (Quote) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node23_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node24_delete(self):
        """testing when node 24 (Quote) is deleted"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node19_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node24_duplicate(self):
        """testing when node 24 (Quote) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node19_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node25_delete(self):
        """testing when node 25 (Value_Label2) is deleted"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node25_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("ContactPhoneNumber key missing", cm.exception.message)

    def test_vaccine_date_node25_duplicate(self):
        """testing when node 25 (Value_Label2) is duplicate"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node25_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("ContactPhoneNumber key missing", cm.exception.message)

    def test_vaccine_date_node26_delete(self):
        """testing when node 26 (Quote) is delete"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node26_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node26_duplicate(self):
        """testing when node 26 (Quote) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node26_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node27_modify(self):
        """testing when node 27 (':') is modified"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node27_modify.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node28_delete(self):
        """testing when node 28 (Quote) is deleted"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node28_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node28_duplicate(self):
        """testing when node 28 (Quote) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node28_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node29_delete(self):
        """testing when node 29 (Value2) is deleted"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node29_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("phone_number must be 9 digits", cm.exception.message)

    def test_vaccine_date_node29_duplicate(self):
        """testing when node 29 (Quote) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node29_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("phone_number must be 9 digits", cm.exception.message)

    def test_vaccine_date_node30_delete(self):
        """testing when node 30 (Quote) is deleted"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node30_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node30_duplicate(self):
        """testing when node 30 (Quote) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node30_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node31_modify(self):
        """testing when node 31 ('"') is modified"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node31_modify.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node32_modify(self):
        """testing when node 32 ('PatientSystemID') is modified"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node32_modify.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("PatientSystemID key missing", cm.exception.message)

    def test_vaccine_date_node33_modify(self):
        """testing when node 33 ('"') is modified"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node33_modify.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node34_modify(self):
        """testing when node 34 ('"') is modified"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node34_modify.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node35_modify(self):
        """testing when node 35 ('regex') is modified"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node35_modify.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("SystemID must be 32 characters long", cm.exception.message)

    def test_vaccine_date_node36_modify(self):
        """testing when node 36('"') is modified"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node36_modify.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node37_modify(self):
        """testing when node 37 ('"') is modified"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node37_modify.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node38_modify(self):
        """testing when node 38 ('ContactPhoneNumber') is modified"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node27_modify.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node39_modify(self):
        """testing when node 39 ('"') is modified"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node27_modify.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node40_modify(self):
        """testing when node 40 ('"') is modified"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node40_modify.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node41_delete(self):
        """testing when node 41 (Prefix) is deleted"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node41_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("phone_number must be 9 digits", cm.exception.message)

    def test_vaccine_date_node41_duplicate(self):
        """testing when node 41 (Prefix) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node41_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("phone_number must be 9 digits", cm.exception.message)

    def test_vaccine_date_node42_delete(self):
        """testing when node 42 (Number) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node42_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("phone_number must be 9 digits", cm.exception.message)

    def test_vaccine_date_node42_duplicate(self):
        """testing when node 42 (Prefix) is duplicated"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node42_duplicate.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node43_modify(self):
        """testing when node 43 ('"') is modified"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node43_modify.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", cm.exception.message)

    def test_vaccine_date_node44_modify(self):
        """testing when node 44 ('+34') is modified"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node44_modify.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("phone_number must be 9 digits", cm.exception.message)

    def test_vaccine_date_node45_modify(self):
        """testing when node 45 ('regex') is modified"""
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            test_file = "node45_modify.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("phone_number must be 9 digits", cm.exception.message)


if __name__ == '__main__':
    unittest.main()
