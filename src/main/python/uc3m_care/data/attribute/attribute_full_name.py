"""Class for the attribute FullName"""

from uc3m_care.data.attribute.attribute import Attribute


# pylint: disable=too-few-public-methods
class FullName(Attribute):
    """Class for the attribute FullName"""
    NAME_SURNAME_NOT_VALID = "name surname is not valid"
    _validation_pattern = r"^(?=^.{1,30}$)(([a-zA-Z]+\s)+[a-zA-Z]+)$"
    _validation_error_message = NAME_SURNAME_NOT_VALID
