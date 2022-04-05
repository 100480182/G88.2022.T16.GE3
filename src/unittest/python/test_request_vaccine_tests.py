import unittest
from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException
from test_utils import TestUtils


class MyTestCase(unittest.TestCase):
    """test file for request_vaccination_id()"""

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

    def test_request_vaccine_ecv1(self):
        """testing valid REGULAR registration"""
        my_manager = VaccineManager()
        my_result = my_manager.request_vaccination_id(patient_id=self.patient_id,
                                                      registration_type=self.registration_type,
                                                      name_surname=self.name_surname,
                                                      phone_number=self.phone_number,
                                                      age=self.age)
        self.assertEqual("2e7ba4f8fc1936352c06a3f200720546", my_result)
        # check that the values has been stored into the file
        found_file = False
        patient_registry_data = TestUtils.read_json_file(TestUtils.patient_registry)
        for patient in patient_registry_data:
            if patient["_VaccinePatientRegister__patient_id"] == self.patient_id:
                found_file = True
        self.assertTrue(found_file)

    def test_request_vaccine_ecv2(self):
        """testing valid FAMILY registration"""
        my_manager = VaccineManager()
        self.registration_type = "FAMILY"
        my_result = my_manager.request_vaccination_id(patient_id=self.patient_id,
                                                      registration_type=self.registration_type,
                                                      name_surname=self.name_surname,
                                                      phone_number=self.phone_number,
                                                      age=self.age)
        self.assertEqual("7944221369d4195e9e74f5aca8c32a50", my_result)
        # check that the values has been stored into the file
        found_file = False
        patient_registry_data = TestUtils.read_json_file(TestUtils.patient_registry)
        for patient in patient_registry_data:
            if patient["_VaccinePatientRegister__patient_id"] == self.patient_id:
                found_file = True
        self.assertTrue(found_file)

    def test_request_vaccine_patient_id_ecnv1(self):
        """testing invalid patient id"""
        with self.assertRaises(VaccineManagementException) as ex:
            my_manager = VaccineManager()
            # ID is not a UUID
            self.patient_id = "HELLO WORLD"
            my_manager.request_vaccination_id(patient_id=self.patient_id,
                                              registration_type=self.registration_type,
                                              name_surname=self.name_surname,
                                              phone_number=self.phone_number,
                                              age=self.age)
        self.assertEqual("Id received is not a UUID", ex.exception.message)

    def test_request_vaccine_patient_id_ecnv2(self):
        """testing invalid patient id"""
        with self.assertRaises(VaccineManagementException) as ex:
            my_manager = VaccineManager()
            # ID is a non-v4 UUID
            self.patient_id = "e19cca80-bb93-32aa-ab0f-780b0caa7d46"
            my_manager.request_vaccination_id(patient_id=self.patient_id,
                                              registration_type=self.registration_type,
                                              name_surname=self.name_surname,
                                              phone_number=self.phone_number,
                                              age=self.age)
        self.assertEqual("Invalid UUID v4 format", ex.exception.message)

    def test_request_vaccine_patient_id_ecnv3(self):
        """testing invalid patient id"""
        with self.assertRaises(VaccineManagementException) as ex:
            my_manager = VaccineManager()
            # ID not a string
            self.patient_id = 1
            my_manager.request_vaccination_id(patient_id=self.patient_id,
                                              registration_type=self.registration_type,
                                              name_surname=self.name_surname,
                                              phone_number=self.phone_number,
                                              age=self.age)
        self.assertEqual("patient_id must be a string value", ex.exception.message)

    def test_request_vaccine_patient_id_ecnv4(self):
        """testing invalid patient id"""
        with self.assertRaises(VaccineManagementException) as ex:
            my_manager = VaccineManager()
            # ID is empty
            self.patient_id = ""
            my_manager.request_vaccination_id(patient_id=self.patient_id,
                                              registration_type=self.registration_type,
                                              name_surname=self.name_surname,
                                              phone_number=self.phone_number,
                                              age=self.age)
        self.assertEqual("Id received is not a UUID", ex.exception.message)

    def test_request_vaccine_reg_type_ecnv5(self):
        """testing invalid registration"""
        with self.assertRaises(VaccineManagementException) as ex:
            my_manager = VaccineManager()
            # REGSITRATION_TYPE invalid
            self.registration_type = "REGULA"
            my_manager.request_vaccination_id(patient_id=self.patient_id,
                                              registration_type=self.registration_type,
                                              name_surname=self.name_surname,
                                              phone_number=self.phone_number,
                                              age=self.age)
        self.assertEqual("registration_type must be REGULAR or FAMILY", ex.exception.message)

    def test_request_vaccine_reg_type_ecnv6(self):
        """testing invalid registration"""
        with self.assertRaises(VaccineManagementException) as ex:
            my_manager = VaccineManager()
            # REGSITRATION_TYPE empty
            self.registration_type = 1
            my_manager.request_vaccination_id(patient_id=self.patient_id,
                                              registration_type=self.registration_type,
                                              name_surname=self.name_surname,
                                              phone_number=self.phone_number,
                                              age=self.age)
        self.assertEqual("registration_type must be a string value", ex.exception.message)

    def test_request_vaccine_reg_type_ecnv7(self):
        """testing invalid registration"""
        with self.assertRaises(VaccineManagementException) as ex:
            my_manager = VaccineManager()
            # REGSITRATION_TYPE empty
            self.registration_type = ""
            my_manager.request_vaccination_id(patient_id=self.patient_id,
                                              registration_type=self.registration_type,
                                              name_surname=self.name_surname,
                                              phone_number=self.phone_number,
                                              age=self.age)
        self.assertEqual("registration_type must be REGULAR or FAMILY", ex.exception.message)

    def test_request_vaccine_name_ecnv8(self):
        """testing invalid name"""
        with self.assertRaises(VaccineManagementException) as ex:
            my_manager = VaccineManager()
            # NAME_SURNAME has more than 30 characters
            self.name_surname = "JOSEJOSEJOSEJOSE LOPEZLOPEZLOPEZ"
            my_manager.request_vaccination_id(patient_id=self.patient_id,
                                              registration_type=self.registration_type,
                                              name_surname=self.name_surname,
                                              phone_number=self.phone_number,
                                              age=self.age)
        self.assertEqual("name_surname must be 30 characters or less", ex.exception.message)

    def test_request_vaccine_name_ecnv9(self):
        """testing invalid name"""
        with self.assertRaises(VaccineManagementException) as ex:
            my_manager = VaccineManager()
            # NAME_SURNAME has no space
            self.name_surname = "JOSE"
            my_manager.request_vaccination_id(patient_id=self.patient_id,
                                              registration_type=self.registration_type,
                                              name_surname=self.name_surname,
                                              phone_number=self.phone_number,
                                              age=self.age)
        self.assertEqual("name_surname must have at least one space", ex.exception.message)

    def test_request_vaccine_name_ecnv10(self):
        """testing invalid name"""
        with self.assertRaises(VaccineManagementException) as ex:
            my_manager = VaccineManager()
            # NAME_SURNAME has only spaces
            self.name_surname = "   "
            my_manager.request_vaccination_id(patient_id=self.patient_id,
                                              registration_type=self.registration_type,
                                              name_surname=self.name_surname,
                                              phone_number=self.phone_number,
                                              age=self.age)
        self.assertEqual("name_surname can't have spaces at beginning or end", ex.exception.message)

    def test_request_vaccine_name_ecnv11(self):
        """testing invalid name"""
        with self.assertRaises(VaccineManagementException) as ex:
            my_manager = VaccineManager()
            # NAME_SURNAME is not a string
            self.name_surname = 1
            my_manager.request_vaccination_id(patient_id=self.patient_id,
                                              registration_type=self.registration_type,
                                              name_surname=self.name_surname,
                                              phone_number=self.phone_number,
                                              age=self.age)
        self.assertEqual("name_surname must be a string value", ex.exception.message)

    def test_request_vaccine_name_ecnv12(self):
        """testing invalid name"""
        with self.assertRaises(VaccineManagementException) as ex:
            my_manager = VaccineManager()
            # NAME_SURNAME is an empty string
            self.name_surname = ""
            my_manager.request_vaccination_id(patient_id=self.patient_id,
                                              registration_type=self.registration_type,
                                              name_surname=self.name_surname,
                                              phone_number=self.phone_number,
                                              age=self.age)
        self.assertEqual("name_surname must have at least one space", ex.exception.message)

    def test_request_vaccine_phone_number_ecnv13(self):
        """testing invalid phone number"""
        with self.assertRaises(VaccineManagementException) as ex:
            my_manager = VaccineManager()
            # PHONE_NUMBER not in string format
            self.phone_number = 341234567899
            my_manager.request_vaccination_id(patient_id=self.patient_id,
                                              registration_type=self.registration_type,
                                              name_surname=self.name_surname,
                                              phone_number=self.phone_number,
                                              age=self.age)
        self.assertEqual("phone_number must be a string", ex.exception.message)

    def test_request_vaccine_phone_number_ecnv14(self):
        """testing invalid phone number"""
        with self.assertRaises(VaccineManagementException) as ex:
            my_manager = VaccineManager()
            # PHONE_NUMBER longer than 9 digits
            self.phone_number = "+341234567899"
            my_manager.request_vaccination_id(patient_id=self.patient_id,
                                              registration_type=self.registration_type,
                                              name_surname=self.name_surname,
                                              phone_number=self.phone_number,
                                              age=self.age)
        self.assertEqual("phone_number must be 9 digits", ex.exception.message)

    def test_request_vaccine_phone_number_ecnv15(self):
        """testing invalid phone number"""
        with self.assertRaises(VaccineManagementException) as ex:
            my_manager = VaccineManager()
            # PHONE_NUMBER shorter than 9 digits
            self.phone_number = "+3412345678"
            my_manager.request_vaccination_id(patient_id=self.patient_id,
                                              registration_type=self.registration_type,
                                              name_surname=self.name_surname,
                                              phone_number=self.phone_number,
                                              age=self.age)
        self.assertEqual("phone_number must be 9 digits", ex.exception.message)

    def test_request_vaccine_phone_number_ecnv16(self):
        """testing invalid phone number"""
        with self.assertRaises(VaccineManagementException) as ex:
            my_manager = VaccineManager()
            # PHONE_NUMBER has letters
            self.phone_number = "+34abc456789"
            my_manager.request_vaccination_id(patient_id=self.patient_id,
                                              registration_type=self.registration_type,
                                              name_surname=self.name_surname,
                                              phone_number=self.phone_number,
                                              age=self.age)
        self.assertEqual("phone_number must contain only digits", ex.exception.message)

    def test_request_vaccine_phone_number_ecnv17(self):
        """testing invalid phone number"""
        with self.assertRaises(VaccineManagementException) as ex:
            my_manager = VaccineManager()
            # PHONE_NUMBER doesn't begin with Spanish country code (+34)
            self.phone_number = "+11123456789"
            my_manager.request_vaccination_id(patient_id=self.patient_id,
                                              registration_type=self.registration_type,
                                              name_surname=self.name_surname,
                                              phone_number=self.phone_number,
                                              age=self.age)
        self.assertEqual("phone_number must begin with +34", ex.exception.message)

    def test_request_vaccine_age_ecnv18(self):
        """testing invalid age"""
        with self.assertRaises(VaccineManagementException) as ex:
            my_manager = VaccineManager()
            # AGE less than 6
            self.age = 5
            my_manager.request_vaccination_id(patient_id=self.patient_id,
                                              registration_type=self.registration_type,
                                              name_surname=self.name_surname,
                                              phone_number=self.phone_number,
                                              age=self.age)
        self.assertEqual("age must be 6 and older", ex.exception.message)

    def test_request_vaccine_age_ecnv19(self):
        """testing invalid phone number"""
        with self.assertRaises(VaccineManagementException) as ex:
            my_manager = VaccineManager()
            # AGE greater than 125
            self.age = 126
            my_manager.request_vaccination_id(patient_id=self.patient_id,
                                              registration_type=self.registration_type,
                                              name_surname=self.name_surname,
                                              phone_number=self.phone_number,
                                              age=self.age)
        self.assertEqual("age must not exceed 125", ex.exception.message)

    def test_request_vaccine_age_ecnv20(self):
        """testing invalid phone number"""
        with self.assertRaises(VaccineManagementException) as ex:
            my_manager = VaccineManager()
            # AGE is not an integer
            self.age = "1e"
            my_manager.request_vaccination_id(patient_id=self.patient_id,
                                              registration_type=self.registration_type,
                                              name_surname=self.name_surname,
                                              phone_number=self.phone_number,
                                              age=self.age)
        self.assertEqual("age must be an integer", ex.exception.message)


if __name__ == '__main__':
    unittest.main()
