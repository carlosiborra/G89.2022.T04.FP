"""Class for the attribute PhoneNumber"""

from uc3m_care.data.attribute.attribute import Attribute


# pylint: disable=too-few-public-methods
class RegistrationType(Attribute):
    """Class for the attribute PhoneNumber"""
    REGISTRATION_TYPE_NOT_VALID = "Registration type is nor valid"
    _validation_pattern = r"(Regular|Family)"
    _validation_error_message = REGISTRATION_TYPE_NOT_VALID
