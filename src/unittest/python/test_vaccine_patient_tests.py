import unittest
import json
import os
from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException
from uc3m_care import VaccinationAppoinment
from test_utils import TestUtils

class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, True)

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

        self.patient_id2 = "bf4d3481-12ff-4093-a6ff-a295fdfe7af1"
        self.registration_type2 = "REGULAR"
        self.name_surname2 = "BRAD SMITH"
        self.phone_number2 = "+34987654321"
        self.age2 = 50

        self.patient_id3 = "ea194706-0933-4d97-a3e7-ee2e6d1542a8"
        self.registration_type3 = "REGULAR"
        self.name_surname3 = "JOE BIDEN"
        self.phone_number3 = "+34678999821"
        self.age3 = 39
        self.setUpClass()

    def test_vaccine_patient_1_2_F(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            my_manager.vaccine_patient("123")
        self.assertEqual("date_signature is invalid", err.exception.message)

    def test_vaccine_patient_1_3_5_F(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            my_manager.request_vaccination_id(patient_id=self.patient_id,
                                              registration_type=self.registration_type,
                                              name_surname=self.name_surname,
                                              phone_number=self.phone_number,
                                              age=self.age)
            signature = my_manager.get_vaccine_date("valid.json")
            my_manager.vaccination_appointments = "epicfail"
            my_manager.vaccine_patient(signature)
        self.assertEqual("vaccination_appointments file not found", err.exception.message)

    def test_vaccine_patient_1_3_4_6_F(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            my_manager.request_vaccination_id(patient_id=self.patient_id,
                                              registration_type=self.registration_type,
                                              name_surname=self.name_surname,
                                              phone_number=self.phone_number,
                                              age=self.age)
            signature = my_manager.get_vaccine_date("valid.json")
            # overwrite vaccine_appointments file so not valid json format
            with open(my_manager.vaccination_appointments, 'w') as file:
                file.write("&")
            # NEED TO HAVE THIS ^^ W/O MESSING UP REST OF TESTS
            my_manager.vaccine_patient(signature)
        self.assertEqual("vaccination_appointments file is not in valid JSON format", err.exception.message)

    def test_vaccine_patient_1_3_4_7_9_10_F(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            my_manager.request_vaccination_id(patient_id=self.patient_id,
                                              registration_type=self.registration_type,
                                              name_surname=self.name_surname,
                                              phone_number=self.phone_number,
                                              age=self.age)
            signature = my_manager.get_vaccine_date("valid.json")
            TestUtils.clear_json_file(my_manager.vaccination_appointments)
            my_manager.vaccine_patient(signature)
        self.assertEqual("date_signature not found in vaccination_appointments", err.exception.message)


    def test_vaccine_patient_1_3_4_7_8_7_9_10_F(self):
        with self.assertRaises(VaccineManagementException) as err:
            my_manager = VaccineManager()
            # register three patients
            my_manager.request_vaccination_id(patient_id=self.patient_id,
                                              registration_type=self.registration_type,
                                              name_surname=self.name_surname,
                                              phone_number=self.phone_number,
                                              age=self.age)
            my_manager.request_vaccination_id(patient_id=self.patient_id2,
                                              registration_type=self.registration_type2,
                                              name_surname=self.name_surname2,
                                              phone_number=self.phone_number2,
                                              age=self.age2)
            my_manager.request_vaccination_id(patient_id=self.patient_id3,
                                              registration_type=self.registration_type3,
                                              name_surname=self.name_surname3,
                                              phone_number=self.phone_number3,
                                              age=self.age3)
            my_manager.get_vaccine_date("valid2.json")
            my_manager.get_vaccine_date("valid3.json")
            signature = my_manager.get_vaccine_date("valid.json")

            # delete the one that we have obtained the signature for from vaccination_appointments
            with open(my_manager.vaccination_appointments, "r", encoding="utf-8") as file:
                data = json.load(file)
                for i in range(len(data)):
                    if data[i]["_VaccinationAppoinment__patient_id"] == "e19cca80-bb93-42aa-ab0f-780b0caa7d46":
                        data.pop(i)
                        break
            with open(my_manager.vaccination_appointments, 'w') as file:
                json.dump(data, file)

            # run the method for an error
            my_manager.vaccine_patient(signature)
        self.assertEqual("date_signature not found in vaccination_appointments", err.exception.message)

    def test_vaccine_patient_1_3_4_7_9_11_12_14_15_F(self):
        # valid, just the vaccination_administration file doesn't exist
        my_manager = VaccineManager()
        my_manager.request_vaccination_id(patient_id=self.patient_id,
                                          registration_type=self.registration_type,
                                          name_surname=self.name_surname,
                                          phone_number=self.phone_number,
                                          age=self.age)
        signature = my_manager.get_vaccine_date("valid.json")
        TestUtils.clear_json_file(my_manager.vaccination_administration)
        res = my_manager.vaccine_patient(signature)
        self.assertEqual(True, res)

    def test_vaccine_patient_1_3_4_7_8_7_9_11_12_14_15_F(self):
        # valid, just the vaccine_administration file doesn't exist with a loop
        my_manager = VaccineManager()
        my_manager.request_vaccination_id(patient_id=self.patient_id,
                                          registration_type=self.registration_type,
                                          name_surname=self.name_surname,
                                          phone_number=self.phone_number,
                                          age=self.age)
        my_manager.request_vaccination_id(patient_id=self.patient_id2,
                                          registration_type=self.registration_type2,
                                          name_surname=self.name_surname2,
                                          phone_number=self.phone_number2,
                                          age=self.age2)
        my_manager.get_vaccine_date("valid2.json")
        signature = my_manager.get_vaccine_date("valid.json")
        # delete vaccination_administration
        os.remove(my_manager.vaccination_administration)
        res = my_manager.vaccine_patient(signature)
        self.assertEqual(True, res)

    def test_vaccine_patient_1_3_4_7_9_11_12_13_15_F(self):
        # valid, vaccine_administration does exist
        my_manager = VaccineManager()
        my_manager.request_vaccination_id(patient_id=self.patient_id,
                                          registration_type=self.registration_type,
                                          name_surname=self.name_surname,
                                          phone_number=self.phone_number,
                                          age=self.age)
        signature = my_manager.get_vaccine_date("valid.json")
        res = my_manager.vaccine_patient(signature)
        self.assertEqual(True, res)
        pass

    def test_vaccine_patient_1_3_4_7_8_7_9_11_12_13_15_F(self):
        # valid, vaccine_administration does exist with a loop
        my_manager = VaccineManager()
        my_manager.request_vaccination_id(patient_id=self.patient_id,
                                          registration_type=self.registration_type,
                                          name_surname=self.name_surname,
                                          phone_number=self.phone_number,
                                          age=self.age)
        my_manager.request_vaccination_id(patient_id=self.patient_id2,
                                          registration_type=self.registration_type2,
                                          name_surname=self.name_surname2,
                                          phone_number=self.phone_number2,
                                          age=self.age2)
        my_manager.get_vaccine_date("valid2.json")
        signature = my_manager.get_vaccine_date("valid.json")
        res = my_manager.vaccine_patient(signature)
        self.assertEqual(True, res)




if __name__ == '__main__':
    unittest.main()
