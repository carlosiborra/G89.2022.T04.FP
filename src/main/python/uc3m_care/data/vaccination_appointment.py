"""Contains the class Vaccination Appointment"""

from datetime import datetime
import hashlib
import json
from freezegun import freeze_time
from uc3m_care.data.attribute.attribute_phone_number import PhoneNumber
from uc3m_care.data.attribute.attribute_patient_system_id import PatientSystemId
from uc3m_care.data.attribute.attribute_date_signature import DateSignature
from uc3m_care.data.vaccination_log import VaccinationLog
from uc3m_care.data.cancelation_messages import CancelationMessage
from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.storage.appointments_json_store import AppointmentsJsonStore
from uc3m_care.storage.appointments_cancel_store import AppointmentsCancelStore
from uc3m_care.parser.appointment_json_parser import AppointmentJsonParser

# pylint: disable=too-many-instance-attributes
from uc3m_care.data.attribute.attribute_cancelation_type import CancelationType
from uc3m_care.data.attribute.attribute_signature_date import SignatureDate
from uc3m_care.data.attribute.attribute_reason import Reason


class VaccinationAppointment:
    """Class representing an appointment  for the vaccination of a patient"""
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

    def __init__(self, patient_sys_id, patient_phone_number, days):
        self.__alg = "SHA-256"
        self.__type = "DS"
        self.__patient_sys_id = PatientSystemId(patient_sys_id).value
        patient = VaccinePatientRegister.create_patient_from_patient_system_id(
            self.__patient_sys_id)
        self.__patient_id = patient.patient_id
        self.__phone_number = PhoneNumber(patient_phone_number).value
        justnow = datetime.utcnow()
        self.__issued_at = datetime.timestamp(justnow)
        if days == 0:
            self.__appointment_date = 0
        else:
            # timestamp is represented in seconds.microseconds
            # age must be expressed in seconds to be added to the timestamp
            self.__appointment_date = self.__issued_at + (days * 24 * 60 * 60)
        self.__date_signature = self.vaccination_signature

    def __signature_string(self) -> str:
        """Composes the string to be used for generating the key for the date"""
        return "{alg:" + self.__alg + ",typ:" + self.__type + ",patient_sys_id:" + \
               self.__patient_sys_id + ",issuedate:" + self.__issued_at.__str__() + \
               ",vaccinationtiondate:" + self.__appointment_date.__str__() + "}"

    @property
    def patient_id(self):
        """Property that represents the guid of the patient"""
        return self.__patient_id

    @patient_id.setter
    def patient_id(self, value):
        self.__patient_id = value

    @property
    def patient_sys_id(self):
        """Property that represents the patient_sys_id of the patient"""
        return self.__patient_sys_id

    @patient_sys_id.setter
    def patient_sys_id(self, value):
        self.__patient_sys_id = value

    @property
    def phone_number(self):
        """Property that represents the phone number of the patient"""
        return self.__phone_number

    @phone_number.setter
    def phone_number(self, value):
        self.__phone_number = PhoneNumber(value).value

    @property
    def vaccination_signature(self):
        """Returns the sha256 signature of the date"""
        return hashlib.sha256(self.__signature_string().encode()).hexdigest()

    @property
    def issued_at(self):
        """Returns the issued at value"""
        return self.__issued_at

    @issued_at.setter
    def issued_at(self, value):
        self.__issued_at = value

    @property
    def appointment_date(self):
        """Returns the vaccination date"""
        return self.__appointment_date

    @property
    def date_signature(self):
        """Returns the SHA256 """
        return self.__date_signature

    def save_appointment(self):
        """saves the appointment in the appointments store"""
        appointments_store = AppointmentsJsonStore()
        appointments_store.add_item(self)

    @classmethod
    def get_appointment_from_date_signature(cls, date_signature):
        """returns the vaccination appointment object for the date_signature received"""
        appointments_store = AppointmentsJsonStore()
        appointment_record = appointments_store.find_item(DateSignature(date_signature).value)

        if appointment_record is None:
            raise VaccineManagementException(CancelationMessage.SIGNATURE_NOT_FOUND)
        freezer = freeze_time(
            datetime.fromtimestamp(appointment_record["_VaccinationAppointment__issued_at"]))
        freezer.start()

        # We get the issued at date timestamp from the created appointment_record
        current_date = appointment_record["_VaccinationAppointment__issued_at"]

        # We get the vaccination date timestamp from the created appointment_record
        vaccination_date = appointment_record["_VaccinationAppointment__appointment_date"]

        # Get the |days left - the timestamp| / number of days rounded
        days_left = days_left_funct(vaccination_date, current_date)

        appointment = cls(appointment_record["_VaccinationAppointment__patient_sys_id"],
                          appointment_record["_VaccinationAppointment__phone_number"],
                          days_left)
        freezer.stop()
        return appointment

    @classmethod
    def create_appointment_from_json_file(cls, json_file, date):
        """returns the vaccination appointment for the received input json file"""
        # Check if date is in the correct iso format
        # The easiest way is to do this is by checking ISO format, takes into account everything
        try:
            # Same as in get_vaccine_date, get date and actual_time
            vaccination_date = datetime.fromisoformat(date).timestamp()
        except Exception as ex:
            raise VaccineManagementException(
                VaccinationAppointment.WRONG_VACCINATION_DATE_FORMAT) from ex

        # Get the actual timestamp (for operation reasons) - frozen
        current_date = datetime.now().timestamp()

        # If vaccination_date is equal or earlier than actual date, VaccineManagementException
        if datetime.fromtimestamp(vaccination_date).date() \
                <= datetime.fromtimestamp(current_date).date():
            raise VaccineManagementException(
                VaccinationAppointment.DATE_EQUAL_EARLIER)

        # Get the |days left - the timestamp| / number of days rounded
        days_left = days_left_funct(vaccination_date, current_date)

        # Instead of 10 days, the difference of the appointment days
        appointment_parser = AppointmentJsonParser(json_file)
        new_appointment = cls(
            appointment_parser.json_content[appointment_parser.PATIENT_SYSTEM_ID_KEY],
            appointment_parser.json_content[appointment_parser.CONTACT_PHONE_NUMBER_KEY],
            days_left)
        return new_appointment

    @classmethod
    def cancel_appointment_from_json_file(cls, input_file):
        """returns date_signature of the cancelled appointment"""
        # This import must be created here in order to prevent cyclic call errors
        from uc3m_care import JSON_FILES_PATH
        appointment_file = JSON_FILES_PATH + "store_date.json"
        vaccination_file = JSON_FILES_PATH + "store_vaccine.json"
        cancellation_file = JSON_FILES_PATH + "store_cancellation.json"

        # We open the input_file - get date signature
        file = cls.open_input_file_json(input_file)

        # Check if date_signature exists in input file and save its value
        try:
            date_signature = file["date_signature"]
        except Exception as ex:
            raise VaccineManagementException(VaccinationAppointment.NO_DATE_SIGNATURE) from ex

        # Check if cancelation_type exists in input file
        try:
            cancellation_type = file["cancelation_type"]
        except Exception as ex:
            raise VaccineManagementException(VaccinationAppointment.NO_CANCELATION_TYPE) from ex

        # Check if reason exists in input file
        try:
            reason = file["reason"]
        except Exception as ex:
            raise VaccineManagementException(VaccinationAppointment.NO_REASON) from ex

        # We check date_signature attribute
        SignatureDate(date_signature).value

        # We check cancellation_type attribute
        CancelationType(cancellation_type).value

        # We check reason attribute
        Reason(reason).value

        # APPOINTMENT
        # We open the store_date.json file w/ the appointments
        cls.open_appointment_file_json(appointment_file, date_signature)

        # Vaccination log
        # We open the store_vaccine.json file and check if date_signature already vaccinated
        cls.open_vaccination_file_json(date_signature, vaccination_file)

        # store_cancellation
        # We open the store_cancellation.json file and check if date_signature already there
        cls.open_cancelation_file_json(cancellation_file, date_signature)

        # After checking everything, we will cancel the given appointment
        file_store = AppointmentsCancelStore()
        file_store.add_item_to_cancel_store(input_file)

        # After all the checks and creation of the cancellation, return date_signature
        return date_signature

    @classmethod
    def open_input_file_json(cls, input_file):
        """opens the input file"""
        try:
            with open(input_file, "r", encoding="utf-8", newline="") as file:
                file = json.load(file)
        except FileNotFoundError as ex:
            raise VaccineManagementException(VaccinationAppointment.FILE_NOT_FOUND) from ex
        except json.JSONDecodeError as ex:
            raise VaccineManagementException(VaccinationAppointment.JEDWJF) from ex
        # Check if input_file is composed by 3 elements
        if len(file) != 3:
            raise VaccineManagementException(VaccinationAppointment.WRONG_N_ELEM)
        return file

    @classmethod
    def open_appointment_file_json(cls, appointment_file, date_signature):
        """opens the appointment file"""
        try:
            with open(appointment_file, "r", encoding="utf-8", newline="") as appoint_file:
                appoint_file = json.load(appoint_file)
        except FileNotFoundError as ex:
            raise VaccineManagementException(
                VaccinationAppointment.APPOINTMENT_FILE_DOES_NOT_EXIST) from ex
        except json.JSONDecodeError as ex:
            raise VaccineManagementException(
                "JSON Decode Error - Wrong JSON Format") from ex
        # We search for an appointment with the given date_signature
        appointment_found = False
        for i in range(len(appoint_file)):
            if appoint_file[i]["_VaccinationAppointment__date_signature"] == date_signature:
                appointment_index = i
                appointment_found = True
                break
            continue

        # If we did not encounter the date_signature - exception
        if appointment_found is False:
            raise VaccineManagementException(
                VaccinationAppointment.APPOINTMENT_DOES_NOT_EXIST)
        # Get the actual timestamp (for operation reasons) - frozen specified by each test
        current_date = datetime.now().timestamp()
        if datetime.fromtimestamp(
                appoint_file[appointment_index]["_VaccinationAppointment__appointment_date"]) \
                .date() < datetime.fromtimestamp(current_date).date():
            raise VaccineManagementException(VaccinationAppointment.APPOINTMENT_PASSED)

    @classmethod
    def open_cancelation_file_json(cls, cancellation_file, date_signature):
        """opens the cancelation file"""
        try:
            with open(cancellation_file, "r", encoding="utf-8", newline="") as cancel_file:
                cancel_file = json.load(cancel_file)
        except FileNotFoundError as ex:
            raise VaccineManagementException(
                VaccinationAppointment.CANCELATION_FILE_DOES_NOT_EXIST) from ex
        except json.JSONDecodeError as ex:
            raise VaccineManagementException(
                "JSON Decode Error - Wrong JSON Format") from ex
        # We search for a cancellation with the given date_signature
        for i in range(len(cancel_file)):
            if cancel_file[i]["date_signature"] == date_signature:
                raise VaccineManagementException(
                    VaccinationAppointment.APPOINTMENT_CANCELLED)
            continue

    @classmethod
    def open_vaccination_file_json(cls, date_signature, vaccination_file):
        """opens the vaccination file"""
        try:
            with open(vaccination_file, "r", encoding="utf-8", newline="") as vaccine_file:
                vaccine_file = json.load(vaccine_file)
        except FileNotFoundError as ex:
            raise VaccineManagementException(
                VaccinationAppointment.VACCINATION_STORE_DOES_NOT_EXIST) from ex
        except json.JSONDecodeError as ex:
            raise VaccineManagementException(
                "JSON Decode Error - Wrong JSON Format") from ex
        # We search for a vaccination with the given date_signature
        for i in range(len(vaccine_file)):
            if vaccine_file[i]["_VaccinationLog__date_signature"] == date_signature:
                raise VaccineManagementException(
                    VaccinationAppointment.VACCINE_ADMINISTERED)
            continue

    def is_valid_today(self):
        """returns true if today is the appointment's date"""
        today = datetime.today().date()
        date_patient = datetime.fromtimestamp(self.appointment_date).date()
        if date_patient != today:
            raise VaccineManagementException(
                VaccinationAppointment.NOT_THE_DATE)
        return True

    def register_vaccination(self):
        """register the vaccine administration"""
        if self.is_valid_today():
            vaccination_log_entry = VaccinationLog(self.date_signature)
            vaccination_log_entry.save_log_entry()
        return True


def days_left_funct(vaccination_date: float, current_date: float) -> int:
    """static function for getting the days_left"""
    days = round(abs(vaccination_date - current_date) / (24 * 60 * 60))
    return days
