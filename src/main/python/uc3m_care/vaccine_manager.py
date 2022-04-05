"""Module """
from datetime import datetime
import uuid
import json
import re
from pathlib import Path
import os
from .vaccine_patient_register import VaccinePatientRegister
from .vaccine_management_exception import VaccineManagementException
from .vaccination_appoinment import VaccinationAppoinment

class VaccineManager:
    """Class for providing the methods for managing the vaccination process"""

    # FOLDER FOR SAVING & READING THE JSON FILES
    # ../../.. CORRESPONDS WITH THE PROJECT MAIN FOLDER
    #json_store = "/Users/davidatwood/Documents/studyabroad/softwaredev/" \
                # "G88.2022.T16.GE3/json/db"
    #json_collection = "/Users/davidatwood/Documents/studyabroad/softwaredev/" \
                    #  "G88.2022.T16.GE3/json/collection"

    json_store = str(Path.home()) + "/PycharmProjects/G88.2022.T16.GE3/json/db"
    json_collection = str(Path.home()) + "/PycharmProjects/G88.2022.T16.GE3/json/collection"

    # FILES WHERE THE INFO WILL BE STORED
    patient_registry = json_store + "/patient_registry.json"
    vaccination_appointments = json_store + "/vaccination_appointments.json"
    vaccination_administration = json_store + "/vaccine_administration.json"

    def __init__(self):
        pass

    @staticmethod
    def validate_guid(patient_id):
        """validates guid"""
        if not isinstance(patient_id, str):
            raise VaccineManagementException("patient_id must be a string value")
        try:
            uuid.UUID(patient_id)
            myregex = re.compile(r'^[0-9A-F]{8}-[0-9A-F]{4}-4[0-9A-F]{3}-[89AB][0-9A-F]{3}-'
                                 r'[0-9A-F]{12}$'
                                 , re.IGNORECASE)
            match = myregex.fullmatch(patient_id)
            if not match:
                raise VaccineManagementException("Invalid UUID v4 format")
        except ValueError as err:
            raise VaccineManagementException("Id received is not a UUID") from err
        return True

    @staticmethod
    def validate_reg_type(registration_type):
        """validates registration_type"""
        if not isinstance(registration_type, str):
            raise VaccineManagementException("registration_type must be a string value")
        if not (registration_type.upper() == "REGULAR" or registration_type.upper() == "FAMILY"):
            raise VaccineManagementException("registration_type must be REGULAR or FAMILY")
        return True

    @staticmethod
    def validate_name(name_surname):
        """validates name_surname"""
        if not isinstance(name_surname, str):
            raise VaccineManagementException("name_surname must be a string value")
        if len(name_surname) > 30:
            raise VaccineManagementException("name_surname must be 30 characters or less")
        if name_surname.strip() != name_surname:
            raise VaccineManagementException("name_surname can't have spaces at beginning or end")
        try:
            name_surname.strip().index(" ")
        except ValueError as err:
            raise VaccineManagementException("name_surname must have at least one space") from err
        return True

    @staticmethod
    def validate_phone_number(phone_number):
        """validates phone_number"""
        if not isinstance(phone_number, str):
            raise VaccineManagementException("phone_number must be a string")
        if not len(phone_number) == 12:
            raise VaccineManagementException("phone_number must be 9 digits")
        if not phone_number[1:].isdigit():
            raise VaccineManagementException("phone_number must contain only digits")
        if phone_number[0:3] != "+34":
            raise VaccineManagementException("phone_number must begin with +34")
        return True

    @staticmethod
    def validate_age(age):
        """validates age"""
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
        """registers patient into patient_registry and returns the SHA 256 System ID"""
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
            except FileExistsError:
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
        raise VaccineManagementException("error")

    def get_vaccine_date(self, input_file):
        """takes patient system ID,
           confirms data in patient_registry,
           and adds patient to vaccination_appointments"""
        # read input file
        try:
            # with open("/Users/davidatwood/Documents/studyabroad/" +
            #           "softwaredev/G88.2022.T16.GE3/src/jsonfiles/" +
            #           input_file, "r", encoding="utf-8") as file:
            with open(str(Path.home()) + "/PycharmProjects/G88.2022.T16.GE3/src/jsonfiles/" +
            input_file, "r", encoding="utf-8") as file:
                appt_request = json.load(file)
        except json.decoder.JSONDecodeError as ex:
            raise VaccineManagementException("appointment request file is not JSON") from ex

        if not appt_request:
            raise VaccineManagementException("appointment request empty")

        # check that system_id and phone_number are valid keys
        try:
            system_id = appt_request["PatientSystemID"]
        except KeyError as ex:
            raise VaccineManagementException("PatientSystemID key missing") from ex
        try:
            phone_number = appt_request["ContactPhoneNumber"]
        except KeyError as ex:
            raise VaccineManagementException("ContactPhoneNumber key missing") from ex

        # check validity of system_id
        if not isinstance(system_id, str):
            raise VaccineManagementException("system_id must be a string")
        if not len(system_id) == 32:
            raise VaccineManagementException("system_id must be 32 characters long")
        if not system_id.isalnum():
            raise VaccineManagementException("system_id must only contain hexadecimals")

        # check validity of phone_number
        self.validate_phone_number(phone_number)

        # get appropriate json file from patient_registry.json
        try:
            with open(self.patient_registry, "r", encoding="utf-8") as file:
                patient_registry = json.load(file)
            patient_found = False
            for patient in patient_registry:
                if system_id == patient["_VaccinePatientRegister__patient_system_id"]:
                    patient_found = True
                    registered = VaccinePatientRegister(
                        patient_id=patient["_VaccinePatientRegister__patient_id"],
                        registration_type=patient["_VaccinePatientRegister__registration_type"],
                        full_name=patient["_VaccinePatientRegister__full_name"],
                        phone_number=patient["_VaccinePatientRegister__phone_number"],
                        age=patient["_VaccinePatientRegister__age"])

            if not patient_found:
                raise VaccineManagementException("patient not found in registry")
                # generate sha256 with hexdigest from patient data, compare to stored sha256
            stored_system_id = registered.patient_system_id
            stored_phone_number = registered.phone_number
            if not system_id == stored_system_id:
                raise VaccineManagementException("system ID does not match data stored in register")
            if not phone_number == stored_phone_number:
                raise VaccineManagementException("phone number does not match number in register")

            # get patient guid to make appointment
            patient_id = registered.patient_id

            new_appointment = VaccinationAppoinment(guid=patient_id,
                                                    patient_sys_id=system_id,
                                                    patient_phone_number=phone_number,
                                                    days=10)

            # add appointment to file, creating the file first if necessary
            try:
                # if file does not exist store the first item
                with open(self.vaccination_appointments, "x", encoding="utf-8", newline="") as file:
                    data = [self.__dict__]
                    json.dump(data, file, indent=2)
            except FileExistsError:
                # if file exists, load the data, append the new item and save it all
                with open(self.vaccination_appointments, "r", encoding="utf-8") as file:
                    # LOAD THE DATA
                    data = json.load(file)
                    # APPEND THE NEW APPOINTMENT
                    data.append(new_appointment.__dict__)
                # Overwrite the data
                with open(self.vaccination_appointments, "w", encoding="utf-8", newline="") as file:
                    json.dump(data, file, indent=2)

            return new_appointment.vaccination_signature

        except FileNotFoundError as ex:
            raise VaccineManagementException("patient registry file not found") from ex


    def vaccine_patient(self, date_signature):
        """takes signature, confirms data is in vaccination_appointments,
           and adds patient to vaccine_administration list.
           returns True if patient is found"""
        if not re.search('[0-9a-fA-F]{64}', date_signature):
            raise VaccineManagementException("date_signature is invalid")

        try:
            with open(self.vaccination_appointments, "r", encoding="utf-8") as file:
                appointments = json.load(file)
        except FileNotFoundError as ex:
            raise VaccineManagementException("vaccination_appointments file not found") from ex
        except json.JSONDecodeError as ex:
            raise VaccineManagementException("vaccination_appointments file is not JSON") from ex

        match = False
        for appointment in appointments:
            if date_signature == appointment["_VaccinationAppoinment__vaccination_signature"]:
                match = True

        if not match:
            raise VaccineManagementException("date_signature not found")

        now = datetime.utcnow()
        new_administration = {"VaccinationSignature": date_signature,
                              "Timestamp": datetime.timestamp(now)}
        # add administration to file, creating the file first if necessary
        try:
            # if file does not exist store the first item
            with open(self.vaccination_administration, "x", encoding="utf-8", newline="") as file:
                data = [self.__dict__]
                json.dump(data, file, indent=2)
        except FileExistsError:
            # if file exists, load the data, append the new item and save it all
            with open(self.vaccination_administration, "r", encoding="utf-8") as file:
                # LOAD THE DATA
                data = json.load(file)
                # APPEND THE NEW ADMINISTRATION
                data.append(new_administration)
            # Overwrite the data
            with open(self.vaccination_administration, "w", encoding="utf-8", newline="") as file:
                json.dump(data, file, indent=2)

        return match
