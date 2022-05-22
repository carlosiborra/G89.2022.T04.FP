"""Class for the attribute PatientSystemId"""

from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.data.magic_str_messages import MagicStrMessage


# pylint: disable=too-few-public-methods
class PatientSystemId(Attribute):
    """Class for the attribute PatientSystemId"""
    PATIENT_ID_NOT_VALID = MagicStrMessage.PATIENT_ID_NOT_VALID
    _validation_pattern = r"[0-9a-fA-F]{32}$"
    _validation_error_message = PATIENT_ID_NOT_VALID
