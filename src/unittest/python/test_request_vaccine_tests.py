import unittest
from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException
from test_utils import TestUtils


class MyTestCase(unittest.TestCase):
    def test_something(self):
        # execute sth to be tested
        # check result w assertion
        self.assertEqual(True, True)

    @classmethod
    def setUpClass(cls) -> None:
        # CREATE THE FOLDERS AND FILES FOR TESTING
        # setUpClass JUST AFTER THE OBJECT HAS BEEN CREATED
        TestUtils.setup_folders()

    @classmethod
    def tearDownClass( cls ) -> None:
        # DELETE THE JSON FILES AT THE END OF THE TEST PROCESS
        # IF YOU WANT TO SEE THE CONTENT OF THE FILES
        # PLEASE COMMENT THE SENTENCE BELOW
        # AND AT THE END OF THE TESTS YOU CAN TAKE A LOOK AT THE CONTENT
        # tearDownClass IS EXECUTED AT THE END OF THE PROCESS
        TestUtils.cleanup_all_folders()


    def setUp(self) -> None:
        """setUp IS EXECUTED ONCE BEFORE EACH TEST"""
        self.patient_id = "e19cca80-bb93-42aa-ab0f-780b0caa7d46"
        self.registration_type = "REGULAR"
        self.name_surname = "JOSE LOPEZ"
        self.phone_number = "+34123456789"
        self.age = 21

    def test_TEST_PATIENT_ID_ECV1(self):
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

    def test_TEST_PATIENT_ID_ECNV1(self):
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            # ID is not a UUID
            self.patient_id = "HELLO WORLD"
            my_result = my_manager.request_vaccination_id(patient_id=self.patient_id,
                                                          registration_type=self.registration_type,
                                                          name_surname=self.name_surname,
                                                          phone_number=self.phone_number,
                                                          age=self.age)
        self.assertEqual("Id received is not a UUID", cm.exception.message)

    def test_TEST_PATIENT_ID_ECNV2(self):
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            # ID is a non-v4 UUID
            self.patient_id = "e19cca80-bb93-32aa-ab0f-780b0caa7d46"
            my_result = my_manager.request_vaccination_id(patient_id=self.patient_id,
                                                          registration_type=self.registration_type,
                                                          name_surname=self.name_surname,
                                                          phone_number=self.phone_number,
                                                          age=self.age)
        self.assertEqual("Invalid UUID v4 format", cm.exception.message)

    def test_TEST_PATIENT_ID_ECNV3(self):
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            # ID not a string
            self.patient_id = 1
            my_result = my_manager.request_vaccination_id(patient_id=self.patient_id,
                                                          registration_type=self.registration_type,
                                                          name_surname=self.name_surname,
                                                          phone_number=self.phone_number,
                                                          age=self.age)
        self.assertEqual("patient_id must be a string value", cm.exception.message)

    def test_TEST_PATIENT_ID_ECNV4(self):
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            # ID is empty
            self.patient_id = ""
            my_result = my_manager.request_vaccination_id(patient_id=self.patient_id,
                                                          registration_type=self.registration_type,
                                                          name_surname=self.name_surname,
                                                          phone_number=self.phone_number,
                                                          age=self.age)
        self.assertEqual("Id received is not a UUID", cm.exception.message)

    def test_TEST_PATIENT_ID_ECNV5(self):
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            # REGSITRATION_TYPE invalid
            self.registration_type = "REGULA"
            my_result = my_manager.request_vaccination_id(patient_id=self.patient_id,
                                                          registration_type=self.registration_type,
                                                          name_surname=self.name_surname,
                                                          phone_number=self.phone_number,
                                                          age=self.age)
        self.assertEqual("registration_type must be either \"REGULAR\" or \"FAMILY\"", cm.exception.message)

    def test_TEST_PATIENT_ID_ECNV6(self):
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            # REGSITRATION_TYPE empty
            self.registration_type = 1
            my_result = my_manager.request_vaccination_id(patient_id=self.patient_id,
                                                          registration_type=self.registration_type,
                                                          name_surname=self.name_surname,
                                                          phone_number=self.phone_number,
                                                          age=self.age)
        self.assertEqual("registration_type must be a string value", cm.exception.message)

    def test_TEST_PATIENT_ID_ECNV7(self):
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            # REGSITRATION_TYPE empty
            self.registration_type = ""
            my_result = my_manager.request_vaccination_id(patient_id=self.patient_id,
                                                          registration_type=self.registration_type,
                                                          name_surname=self.name_surname,
                                                          phone_number=self.phone_number,
                                                          age=self.age)
        self.assertEqual("registration_type must be either \"REGULAR\" or \"FAMILY\"", cm.exception.message)

    def test_TEST_PATIENT_ID_ECNV8(self):
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            # REGSITRATION_TYPE empty
            self.registration_type = ""
            my_result = my_manager.request_vaccination_id(patient_id=self.patient_id,
                                                          registration_type=self.registration_type,
                                                          name_surname=self.name_surname,
                                                          phone_number=self.phone_number,
                                                          age=self.age)
        self.assertEqual("registration_type must be either \"REGULAR\" or \"FAMILY\"", cm.exception.message)

    def test_TEST_PATIENT_ID_ECNV9(self):
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            # NAME_SURNAME has more than 30 characters
            self.registration_type = "JOSEJOSEJOSEJOSE LOPEZLOPEZLOPEZ"
            my_result = my_manager.request_vaccination_id(patient_id=self.patient_id,
                                                          registration_type=self.registration_type,
                                                          name_surname=self.name_surname,
                                                          phone_number=self.phone_number,
                                                          age=self.age)
        self.assertEqual("name_surname must be less than 30 characters", cm.exception.message)

    def test_TEST_PATIENT_ID_ECNV10(self):
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            # NAME_SURNAME has no space
            self.registration_type = "JOSE"
            my_result = my_manager.request_vaccination_id(patient_id=self.patient_id,
                                                          registration_type=self.registration_type,
                                                          name_surname=self.name_surname,
                                                          phone_number=self.phone_number,
                                                          age=self.age)
        self.assertEqual("name_surname must have at least one space", cm.exception.message)

    def test_TEST_PATIENT_ID_ECNV11(self):
        with self.assertRaises(VaccineManagementException) as cm:
            my_manager = VaccineManager()
            # NAME_SURNAME has only spaces
            self.registration_type = "   "
            my_result = my_manager.request_vaccination_id(patient_id=self.patient_id,
                                                          registration_type=self.registration_type,
                                                          name_surname=self.name_surname,
                                                          phone_number=self.phone_number,
                                                          age=self.age)
        self.assertEqual("name_surname must have two strings", cm.exception.message)


if __name__ == '__main__':
    unittest.main()
