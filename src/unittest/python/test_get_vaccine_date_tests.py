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
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            my_manager.request_vaccination_id(patient_id=self.patient_id,
                                              registration_type=self.registration_type,
                                              name_surname=self.name_surname,
                                              phone_number=self.phone_number,
                                              age=self.age)
            test_file = "node1_delete.json"
            res = my_manager.get_vaccine_date(test_file)
        self.assertEqual("appointment request file empty", cm.exception.message)



if __name__ == '__main__':
    unittest.main()
