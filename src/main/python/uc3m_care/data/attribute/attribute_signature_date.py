"""Class for the attribute SignatureDate"""

import re
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


# pylint: disable=too-few-public-methods
class SignatureDate(Attribute):
    """Class for the date_signature"""
    INVALID_DATE_SIGNATURE = "Invalid date_signature"
    DATE_SIGNATURE_NOT_A_STRING = "Invalid date_signature: not a string"
    _validation_pattern = r"^[a-fA-F0-9]{64}$"
    _validation_error_message = "Invalid date_signature"

    # We check that date_signature type is sha256 - 64 bytes hexadecimal
    def _validate(self, attr_value: str) -> str:
        """overrides the validate method to include the validation of  UUID values"""
        try:
            pattern = r"^[a-fA-F0-9]{64}$"
            res = re.fullmatch(pattern, attr_value)
            if not res:
                raise VaccineManagementException(
                    SignatureDate.INVALID_DATE_SIGNATURE)
        except TypeError as ex:
            raise VaccineManagementException(
                SignatureDate.DATE_SIGNATURE_NOT_A_STRING) from ex
        return attr_value
