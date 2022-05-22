"""Contains the class Vaccination Appointment"""


# pylint: disable=too-few-public-methods
class CancelationMessage:
    """Cancellation messages"""
    SIGNATURE_NOT_FOUND = "date_signature is not found"
    WRONG_VACCINATION_DATE_FORMAT = "Wrong vaccination_date format"
    DATE_EQUAL_EARLIER = "vaccination_date equal or earlier than current_date"
    JEDWJF = "JSON Decode Error - Wrong JSON Format"
    FILE_NOT_FOUND = "File is not found"
    NO_REASON = "No reason in input_file"
    NO_CANCELATION_TYPE = "No cancelation_type in input_file"
    NO_DATE_SIGNATURE = "No date_signature in input_file"
    WRONG_N_ELEM = "Wrong number of elements in input_file"
    APPOINTMENT_CANCELLED = "Appointment has already been canceled"
    CANCELATION_FILE_DOES_NOT_EXIST = "The cancellation_file does not exist"
    VACCINE_ADMINISTERED = "Vaccine has already been administered"
    VACCINATION_STORE_DOES_NOT_EXIST = "The vaccination_store does not exist"
    APPOINTMENT_PASSED = "The appointment date received has already passed"
    APPOINTMENT_DOES_NOT_EXIST = "The appointment received does not exist"
    APPOINTMENT_FILE_DOES_NOT_EXIST = "The appointment_file received does not exist"
    NOT_THE_DATE = "Today is not the date"
