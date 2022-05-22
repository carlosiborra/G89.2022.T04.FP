"""Superclass for parsing input json files"""

import json
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.data.cancelation_messages import CancelationMessage


class JsonParser:
    """Subclass of JsonStore for managing the Appointments"""
    _JSON_KEYS = []
    _ERROR_MESSAGES = []
    _json_content = None
    FILE_NOT_FOUND = CancelationMessage.FILE_NOT_FOUND
    WRONG_JSON_FORMAT = CancelationMessage.WRONG_JSON_FORMAT

    def __init__(self, input_file):
        self._input_file = input_file
        self.load_json_content()
        self.validate_json_keys()

    def validate_json_keys(self):
        """Validates the keys stored in JSON_KEYS list"""
        for key, error_message in zip(self._JSON_KEYS, self._ERROR_MESSAGES):
            if key not in self._json_content.keys():
                raise VaccineManagementException(error_message)

    def load_json_content(self):
        """loads the content of the json file in a dictionary"""
        try:
            with open(self._input_file, "r", encoding="utf-8", newline="") as file:
                data = json.load(file)
        except FileNotFoundError as ex:
            # file is not found
            raise VaccineManagementException(JsonParser.FILE_NOT_FOUND) from ex
        except json.JSONDecodeError as ex:
            raise VaccineManagementException(JsonParser.WRONG_JSON_FORMAT) from ex
        self._json_content = data

    @property
    def json_content(self):
        """returns a dictionary with the content of the json file"""
        return self._json_content
