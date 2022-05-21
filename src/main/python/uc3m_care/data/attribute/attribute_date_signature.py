"""Classs for the attribute DateSignature"""
from uc3m_care.data.attribute.attribute import Attribute

#pylint: disable=too-few-public-methods



class DateSignature(Attribute):
    """Class for the attribute DateSignature"""
    DATE_SIGNATURE_FORMAT_NOT_VALID = "date_signature format is not valid"
    _validation_pattern = r"[0-9a-fA-F]{64}$"
    _validation_error_message = DATE_SIGNATURE_FORMAT_NOT_VALID
