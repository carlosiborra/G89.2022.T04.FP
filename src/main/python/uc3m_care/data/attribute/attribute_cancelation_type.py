"""Class for the attribute CancelationType"""

import re
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.data.magic_str_messages import MagicStrMessage


# pylint: disable=too-few-public-methods
class CancelationType(Attribute):
    """Class for the cancelation_type"""
    CANCELATION_TYPE_NOT_A_STRING = MagicStrMessage.CANCELATION_TYPE_NOT_A_STRING
    INVALID_CANCELATION_TYPE = MagicStrMessage.INVALID_CANCELATION_TYPE
    _validation_pattern = r"Final|Temporal"
    _validation_error_message = INVALID_CANCELATION_TYPE

    # We check that cancellation type is either Temporal or final
    def _validate(self, attr_value: str) -> str:
        """overrides the validate method to include the validation of  UUID values"""
        try:
            pattern = r"Final|Temporal"
            res = re.fullmatch(pattern, attr_value)
            if not res:
                raise VaccineManagementException(
                    CancelationType.INVALID_CANCELATION_TYPE)
        except TypeError as ex:
            raise VaccineManagementException(
                CancelationType.CANCELATION_TYPE_NOT_A_STRING) from ex
        return attr_value
