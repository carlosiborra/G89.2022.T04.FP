"""Class for the attribute SignatureDate"""

import re
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.data.magic_str_messages import MagicStrMessage


# pylint: disable=too-few-public-methods
class SignatureDate(Attribute):
    """Class for the date_signature"""
    INVALID_DATE_SIGNATURE = MagicStrMessage.INVALID_DATE_SIGNATURE
    DATE_SIGNATURE_NOT_A_STRING = MagicStrMessage.DATE_SIGNATURE_NOT_A_STRING
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
