"""Class for the attribute CancelationType"""

from uc3m_care.data.attribute.attribute import Attribute

class CancelationType(Attribute):
    _validation_pattern = r"Final|Temporal"
    _validation_error_message = "Invalid cancelation_type"