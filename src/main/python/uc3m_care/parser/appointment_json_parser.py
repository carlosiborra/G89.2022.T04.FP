"""Subclass of JsonParer for parsing inputs of get_vaccine_date"""

from uc3m_care.parser.json_parser import JsonParser
from uc3m_care.data.magic_str_messages import MagicStrMessage


class AppointmentJsonParser(JsonParser):
    """Subclass of JsonParer for parsing inputs of get_vaccine_date"""
    BAD_PHONE_NUMBER_LABEL_ERROR = MagicStrMessage.BAD_PHONE_NUMBER_LABEL_ERROR
    BAD_PATIENT_SYS_ID_LABEL_ERROR = MagicStrMessage.BAD_PATIENT_SYS_ID_LABEL_ERROR
    PATIENT_SYSTEM_ID_KEY = MagicStrMessage.PATIENT_SYSTEM_ID_KEY
    CONTACT_PHONE_NUMBER_KEY = MagicStrMessage.CONTACT_PHONE_NUMBER_KEY

    _JSON_KEYS = [PATIENT_SYSTEM_ID_KEY, CONTACT_PHONE_NUMBER_KEY]
    _ERROR_MESSAGES = [BAD_PATIENT_SYS_ID_LABEL_ERROR, BAD_PHONE_NUMBER_LABEL_ERROR]
