"""Class for the attribute Reason"""

from uc3m_care.data.attribute.attribute import Attribute


class Reason(Attribute):
    _validation_pattern = r"^[\d\w\s]{2,100}$"
    _validation_error_message = "Invalid reason"