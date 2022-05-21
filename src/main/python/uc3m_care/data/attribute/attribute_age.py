"""Class for the attribute age"""

from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


# pylint: disable=too-few-public-methods
class Age(Attribute):
    """Class for the attribute age"""
    AGE_NOT_VALID = "age is not valid"
    _validation_error_message = AGE_NOT_VALID

    def _validate(self, attr_value: str) -> str:
        """Validates the age according to the requirements"""
        if attr_value.isnumeric():
            if int(attr_value) < 6 or int(attr_value) > 125:
                raise VaccineManagementException(self._validation_error_message)
        else:
            raise VaccineManagementException(self._validation_error_message)
        return attr_value
