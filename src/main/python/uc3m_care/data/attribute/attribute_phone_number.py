"""Class for the attribute PhoneNumber"""

from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.data.cancelation_messages import CancelationMessage


# pylint: disable=too-few-public-methods
class PhoneNumber(Attribute):
    """Class for the attribute PhoneNumber"""
    PHONE_NUMBER_NOT_VALID = CancelationMessage.PHONE_NUMBER_NOT_VALID
    _validation_pattern = r"^(\+)[0-9]{11}"
    _validation_error_message = PHONE_NUMBER_NOT_VALID
