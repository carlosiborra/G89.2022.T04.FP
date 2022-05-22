"""Class for the attribute Reason"""

import re
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.data.cancelation_messages import CancelationMessage


# pylint: disable=too-few-public-methods
class Reason(Attribute):
    """Class for the attribute reason"""
    NO_REASON = CancelationMessage.NO_REASON
    REASON_NOT_A_STRING = CancelationMessage.REASON_NOT_A_STRING
    INVALID_REASON = CancelationMessage.INVALID_REASON
    _validation_pattern = r"^[\d\w\s]{2,100}$"
    _validation_error_message = INVALID_REASON

    # We check that reason string has between 2 and 100 characters
    # We also check that it is a string
    def _validate(self, attr_value: str) -> str:
        """overrides the validate method to include the validation of  UUID values"""
        try:
            pattern = r"^[\d\w\s]{2,100}$"
            res = re.fullmatch(pattern, attr_value)
            if not res:
                raise VaccineManagementException(Reason.INVALID_REASON)
        except TypeError as ex:
            raise VaccineManagementException(Reason.REASON_NOT_A_STRING) from ex
        return attr_value
