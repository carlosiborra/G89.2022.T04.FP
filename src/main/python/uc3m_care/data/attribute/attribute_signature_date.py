"""Class for the attribute SignatureDate"""

from uc3m_care.data.attribute.attribute import Attribute


# pylint: disable=too-few-public-methods
class SignatureDate(Attribute):
    """Class for the date_signature"""
    _validation_pattern = r"^[a-fA-F0-9]{64}$"
    _validation_error_message = "Invalid date_signature"
