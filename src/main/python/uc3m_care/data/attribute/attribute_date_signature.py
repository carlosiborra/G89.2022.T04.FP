"""Class for the attribute DateSignature"""

from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.data.magic_str_messages import MagicStrMessage


# pylint: disable=too-few-public-methods
class DateSignature(Attribute):
    """Class for the attribute DateSignature"""
    DATE_SIGNATURE_FORMAT_NOT_VALID = MagicStrMessage.DATE_SIGNATURE_FORMAT_NOT_VALID
    _validation_pattern = r"[0-9a-fA-F]{64}$"
    _validation_error_message = DATE_SIGNATURE_FORMAT_NOT_VALID
