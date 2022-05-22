"""Class for the attribute PhoneNumber"""

from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.data.magic_str_messages import MagicStrMessage


# pylint: disable=duplicate-code
# pylint: disable=too-few-public-methods
class RegistrationType(Attribute):
    """Class for the attribute PhoneNumber"""
    REGISTRATION_TYPE_NOT_VALID = MagicStrMessage.REGISTRATION_TYPE_NOT_VALID
    _validation_pattern = r"(Regular|Family)"
    _validation_error_message = REGISTRATION_TYPE_NOT_VALID
