"""Module """
from .vaccine_patient_register import VaccinePatientRegister
from .vaccine_management_exception import VaccineManagementException
from .vaccination_appoinment import VaccinationAppoinment
import uuid
import json
from pathlib import Path
import os


class VaccineManager:
    """Class for providing the methods for managing the vaccination process"""

    # FOLDER FOR SAVING & READING THE JSON FILES
    # ../../.. CORRESPONDS WITH THE PROJECT MAIN FOLDER
    json_store = "/Users/davidatwood/Documents/studyabroad/softwaredev/G88.2022.T16.GE3/json/db"
    json_collection = "/Users/davidatwood/Documents/studyabroad/softwaredev/G88.2022.T16.GE3/json/collection"

    # json_store = str(Path.home()) + "/PycharmProjects/G88.2022.T16.GE3/json/db"
    # json_collection = str(Path.home()) + "/PycharmProjects/G88.2022.T16.GE3/json/collection"


    # FILES WHERE THE INFO WILL BE STORED
    patient_registry = json_store + "/patient_registry.json"
    vaccination_appointments = json_store + "/vaccination_appointments.json"
    vaccination_administration = json_store + "/vaccine_administration.json"

    def __init__(self):
        pass

    @staticmethod
    def validate_guid(patient_id):
        if not isinstance(patient_id, str):
            raise VaccineManagementException("patient_id must be a string value")
        try:
            myUUID = uuid.UUID(patient_id)
            import re
            myregex = re.compile(r'^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-'
                                 r'[0-9A-F]{12}$'
                                 , re.IGNORECASE)
            x = myregex.fullmatch(patient_id)
            if not x:
                raise VaccineManagementException("Invalid UUID v4 format")
        except ValueError as e:
            raise VaccineManagementException("Id received is not a UUID") from e
        return True

    @staticmethod
    def validate_reg_type(registration_type):
        if not isinstance(registration_type, str):
            raise VaccineManagementException("registration_type must be a string value")
        if not (registration_type.upper() == "REGULAR" or registration_type.upper() == "FAMILY"):
            raise VaccineManagementException("registration_type must be either \"REGULAR\" or \"FAMILY\"")
        return True

    @staticmethod
    def validate_name(name_surname):
        if not isinstance(name_surname, str):
            raise VaccineManagementException("name_surname must be a string value")
        if len(name_surname) > 30:
            raise VaccineManagementException("name_surname must be 30 characters or less")
        if name_surname.strip() != name_surname:
            raise VaccineManagementException("name_surname may not have leading or trailing spaces")
        try:
            name_surname.strip().index(" ")
        except ValueError:
            raise VaccineManagementException("name_surname must have at least one space")
        return True

    @staticmethod
    def validate_phone_number(phone_number):
        if not isinstance(phone_number, str):
            raise VaccineManagementException("phone_number must be a string")
        if len(phone_number) > 12:
            raise VaccineManagementException("phone_number must be no more than 9 digits")
        if len(phone_number) < 12:
            raise VaccineManagementException("phone_number must not be shorter than 9 digits")
        if not phone_number[1:].isdigit():
            raise VaccineManagementException("phone_number must contain only digits")
        if phone_number[0:3] != "+34":
            raise VaccineManagementException("phone_number must begin with +34")
        return True

    @staticmethod
    def validate_age(age):
        if not isinstance(age, int):
            raise VaccineManagementException("age must be an integer")
        if age > 125:
            raise VaccineManagementException("age must not exceed 125")
        if age < 6:
            raise VaccineManagementException("age must be 6 and older")
        return True


    def request_vaccination_id(self,
                               patient_id,
                               registration_type,
                               name_surname,
                               phone_number,
                               age):
        if self.validate_guid(patient_id) and self.validate_reg_type(registration_type) and \
                self.validate_name(name_surname) and self.validate_phone_number(phone_number) and \
                self.validate_age(age):
            my_reg = VaccinePatientRegister(patient_id=patient_id,
                                            registration_type=registration_type,
                                            full_name=name_surname,
                                            phone_number=phone_number,
                                            age=age)
            # save the values into a file
            try:
                # if file does not exist store the first item
                with open(self.patient_registry, "x", encoding="utf-8", newline="") as file:
                    data = [self.__dict__]
                    json.dump(data, file, indent=2)
            except FileExistsError as ex:
                # if file exists, load the data, append the new item and save it all
                with open(self.patient_registry, "r",
                          encoding="utf-8") as file:
                    # LOAD THE DATA
                    data = json.load(file)
                    # APPEND THE NEW REGISTER
                    data.append(my_reg.__dict__)
                # Overwrite the data
                with open(self.patient_registry, "w", encoding="utf-8", newline="") as file:
                    json.dump(data, file, indent=2)

            return my_reg.patient_system_id

    def get_vaccine_date(self, input_file):
        # read input file
        try:
            with open("../../../jsonfiles/" + input_file, "r", encoding="utf-8") as file:
                apptReq = json.load(file)
            # check valid format
            if not apptReq:
                raise VaccineManagementException("appointment request file empty")
        except FileNotFoundError as ex:
            raise VaccineManagementException("appointment request file not found")

        # get appropriate json file from patient_registry.json
        systemID = apptReq["PatientSystemID"]
        phoneNumber = apptReq["ContactPhoneNumber"]

        try:
            with open(self.patient_registry, "r", encoding="utf-8") as file:
                patientRegistry = json.load(file)
            patientFound = False
            for patient in patientRegistry:
                if systemID == patient["_VaccinePatientRegister__patient_system_id"]:
                    patientFound = True
                    registered = VaccinePatientRegister(patient_id=patient["_VaccinePatientRegister__patient_id"],
                                                        registration_type=patient[
                                                            "_VaccinePatientRegister__registration_type"],
                                                        full_name=patient["_VaccinePatientRegister__full_name"],
                                                        phone_number=patient["_VaccinePatientRegister__phone_number"],
                                                        age=patient["_VaccinePatientRegister__age"])

            if not patientFound:
                raise VaccineManagementException("patient not found in registry")

            # generate sha256 with hexdigest from patient data, compare to stored sha256 (patient system id)
            storedSystemID = registered.patient_system_id()
            storedPhoneNumber = registered.phone_number()
            if not systemID == storedSystemID:
                raise VaccineManagementException("system ID does not match data stored in register")
            if not phoneNumber == storedPhoneNumber:
                raise VaccineManagementException("phone number does not match number in register")

            patientID = registered.patient_id()

            new_appointment = VaccinationAppoinment(guid=patientID,
                                                    patient_sys_id= systemID,
                                                    patient_phone_number=phoneNumber,
                                                    days=10)

            # add appointment to file, creating the file first if necessary
            try:
                # if file does not exist store the first item
                with open(self.vaccination_appointments, "x", encoding="utf-8", newline="") as file:
                    data = [self.__dict__]
                    json.dump(data, file, indent=2)
            except FileExistsError as ex:
                # if file exists, load the data, append the new item and save it all
                with open(self.vaccination_appointments, "r", encoding="utf-8") as file:
                    # LOAD THE DATA
                    data = json.load(file)
                    # APPEND THE NEW APPOINTMENT
                    data.append(new_appointment.__dict__)
                # Overwrite the data
                with open(self.vaccination_appointments, "w", encoding="utf-8", newline="") as file:
                    json.dump(data, file, indent=2)

        except FileNotFoundError as ex:
            raise VaccineManagementException("patient registry file not found")


        # return hex string SHA256 thing [hashlib.sha256(self.__signature_string().encode()).hexdigest()]
        # check sha256
        # in case of error, VaccineManagementException
