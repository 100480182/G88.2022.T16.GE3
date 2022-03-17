"""Module """
from .vaccine_patient_register import VaccinePatientRegister
from .vaccine_management_exception import VaccineManagementException
import uuid
import json


class VaccineManager:
    """Class for providing the methods for managing the vaccination process"""

    # FOLDER FOR SAVING & READING THE JSON FILES
    # ../../.. CORRESPONDS WITH THE PROJECT MAIN FOLDER
    json_store = "../../../json/db"
    json_collection = "../../../json/collection"

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

    def request_vaccination_id(self,
                               patient_id,
                               registration_type,
                               name_surname,
                               phone_number,
                               age):
        if self.validate_guid(patient_id):
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
