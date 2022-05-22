"""Class for the attribute PhoneNumber"""

from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.data.magic_str_messages import MagicStrMessage


# pylint: disable=too-few-public-methods
class PhoneNumber(Attribute):
    """Class for the attribute PhoneNumber"""
    PHONE_NUMBER_NOT_VALID = MagicStrMessage.PHONE_NUMBER_NOT_VALID
    _validation_pattern = r"^(\+)[0-9]{11}"
    _validation_error_message = PHONE_NUMBER_NOT_VALID
