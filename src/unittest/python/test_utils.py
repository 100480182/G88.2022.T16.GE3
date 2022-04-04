"""Test setup for the Python unittest module."""
import json
from pathlib import Path
from shutil import rmtree


class TestUtils:
    """Test setup for the Python unittest module."""
    # FOLDER FOR SAVING & READING THE JSON FILES
    #../../.. CORRESPONDS WITH THE PROJECT MAIN FOLDER
    #json_store = "/Users/davidatwood/Documents/studyabroad/softwaredev/G88.2022.T16.GE3/json/db"
    #json_collection = "/Users/davidatwood/Documents/studyabroad/softwaredev/G88.2022.T16.GE3/json/collection"

    json_store = str(Path.home()) + "/PycharmProjects/G88.2022.T16.GE3/json/db"
    json_collection = str(Path.home()) + "/PycharmProjects/G88.2022.T16.GE3/json/collection"

    patient_registry = json_store + "/patient_registry.json"
    vaccination_appointments = json_store + "/vaccination_appointments.json"
    vaccination_administration = json_store + "/vaccine_administration.json"

    @classmethod
    def setup_folders(cls):
        """Create folders for testing."""
        Path(cls.json_store).mkdir(parents=True, exist_ok=True)
        Path(cls.json_collection).mkdir(parents=True, exist_ok=True)
        Path(cls.patient_registry) \
            .touch(mode=0o777, exist_ok=True)
        Path(cls.vaccination_appointments) \
            .touch(mode=0o777, exist_ok=True)
        Path(cls.vaccination_administration) \
            .touch(mode=0o777, exist_ok=True)

        cls.clear_json_file(cls.patient_registry)
        cls.clear_json_file(cls.vaccination_appointments)
        cls.clear_json_file(cls.vaccination_administration)

    @classmethod
    def cleanup_all_folders(cls):
        """Cleanup folders for testing."""
        rmtree(cls.json_store)

    @classmethod
    def read_json_file(cls, path):
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return data

    @classmethod
    def clear_json_file(cls, path):
        with open(path, "w", encoding="utf-8") as file:
            json.dump([], file)
