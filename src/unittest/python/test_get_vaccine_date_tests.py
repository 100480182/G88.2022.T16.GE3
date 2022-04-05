import hashlib
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
        with open(TestUtils.vaccination_appointments, "r", encoding="utf-8", newline = "") as file:
            hash_before = hashlib.md5(file.__str__().encode()).hexdigest()
            print(json.dumps(json.load(file), indent=2))

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

        with open(TestUtils.vaccination_appointments, "r", encoding="utf-8", newline = "") as file:
            hash_after = hashlib.md5(file.__str__().encode()).hexdigest()
            print(json.dumps(json.load(file), indent=2))
        self.assertEqual(hash_before, hash_after)


    def test_vaccine_date_node1_delete(self):
        with open(TestUtils.vaccination_appointments, "r", encoding="utf-8", newline = "") as vac_appts:
            hash_before = hashlib.md5(vac_appts.__str__().encode()).hexdigest()
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node1_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)
        with open(TestUtils.vaccination_appointments, "r", encoding="utf-8", newline = "") as vac_appts:
            hash_after = hashlib.md5(vac_appts.__str__().encode()).hexdigest()
        self.assertEqual(hash_before, hash_after)

    def test_vaccine_date_node1_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node1_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node2_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node2_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node2_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node2_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node3_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node3_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request empty", err.exception.message)

    def test_vaccine_date_node3_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node3_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node4_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node4_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node4_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node4_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node5_modify(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node5_modify.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node6_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node6_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node6_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node6_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node7_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node7_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node7_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node7_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node8_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node8_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node8_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node8_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node9_modify(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node5_modify.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node10_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node10_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node10_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node10_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node11_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node11_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node11_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node11_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node12_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node12_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node12_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node12_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node13_modify(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node13_modify.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node14_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node14_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node14_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node14_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node15_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node15_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node15_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node15_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node16_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node16_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node16_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node16_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node17_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node17_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node17_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node17_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node18_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node18_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("PatientSystemID key missing", err.exception.message)

    def test_vaccine_date_node18_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node18_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("PatientSystemID key missing", err.exception.message)

    def test_vaccine_date_node19_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node19_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node19_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node19_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node20_modify(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node20_modify.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node21_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node21_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node21_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node21_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node22_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node22_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("system_id must be 32 characters long", err.exception.message)

    def test_vaccine_date_node22_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node22_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("system_id must be 32 characters long", err.exception.message)

    def test_vaccine_date_node23_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node23_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node23_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node23_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node24_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node19_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node24_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node19_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node25_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node25_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("ContactPhoneNumber key missing", err.exception.message)

    def test_vaccine_date_node25_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node25_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("ContactPhoneNumber key missing", err.exception.message)

    def test_vaccine_date_node26_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node26_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node26_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node26_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node27_modify(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node27_modify.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node28_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node28_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node28_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node28_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node29_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node29_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("phone_number must be 9 digits", err.exception.message)

    def test_vaccine_date_node29_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node29_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("phone_number must be 9 digits", err.exception.message)

    def test_vaccine_date_node30_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node30_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node30_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node30_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node31_modify(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node31_modify.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node32_modify(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node32_modify.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("PatientSystemID key missing", err.exception.message)

    def test_vaccine_date_node33_modify(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node33_modify.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node34_modify(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node34_modify.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node35_modify(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node35_modify.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("system_id must be 32 characters long", err.exception.message)

    def test_vaccine_date_node36_modify(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node36_modify.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node37_modify(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node37_modify.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node38_modify(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node27_modify.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node39_modify(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node27_modify.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node40_modify(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node40_modify.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node41_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node41_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("phone_number must be 9 digits", err.exception.message)

    def test_vaccine_date_node41_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node41_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("phone_number must be 9 digits", err.exception.message)

    def test_vaccine_date_node42_delete(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node42_delete.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("phone_number must be 9 digits", err.exception.message)

    def test_vaccine_date_node42_duplicate(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node42_duplicate.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node43_modify(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node43_modify.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file has invalid JSON format", err.exception.message)

    def test_vaccine_date_node44_modify(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node44_modify.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("phone_number must be 9 digits", err.exception.message)

    def test_vaccine_date_node45_modify(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            test_file = "node45_modify.json"
            my_manager.get_vaccine_date(test_file)
        self.assertEqual("phone_number must be 9 digits", err.exception.message)


if __name__ == '__main__':
    unittest.main()
