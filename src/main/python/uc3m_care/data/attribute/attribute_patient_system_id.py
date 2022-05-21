"""Classs for the attribute PatientSystemId"""
from uc3m_care.data.attribute.attribute import Attribute


# pylint: disable=too-few-public-methods


class PatientSystemId(Attribute):
    """Classs for the attribute PatientSystemId"""
    PATIENT_ID_NOT_VALID = "patient system id is not valid"
    _validation_pattern = r"[0-9a-fA-F]{32}$"
    _validation_error_message = PATIENT_ID_NOT_VALID
