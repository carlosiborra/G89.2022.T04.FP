"""Contains the class Vaccination Appointment"""
from datetime import datetime
import hashlib
import json
import re
from freezegun import freeze_time
from uc3m_care.data.attribute.attribute_phone_number import PhoneNumber
from uc3m_care.data.attribute.attribute_patient_system_id import PatientSystemId
from uc3m_care.data.attribute.attribute_date_signature import DateSignature
from uc3m_care.data.vaccination_log import VaccinationLog
from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.storage.appointments_json_store import AppointmentsJsonStore
from uc3m_care.parser.appointment_json_parser import AppointmentJsonParser



# pylint: disable=too-many-instance-attributes



class VaccinationAppointment():
    """Class representing an appointment  for the vaccination of a patient"""

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
            # timestamp is represneted in seconds.microseconds
            # age must be expressed in senconds to be added to the timestap
            self.__appointment_date = self.__issued_at + (days * 24 * 60 * 60)
        self.__date_signature = self.vaccination_signature
    SIGNATURE_NOT_FOUND = "date_signature is not found"
    WRONG_VACCINATION_DATE_FORMAT = "Wrong vaccination_date format"
    DATE_EQUAL_EARLIER = "vaccination_date equal or earlier than current_date"
    JEDWJF = "JSON Decode Error - Wrong JSON Format"
    FILE_NOT_FOUND = "File is not found"
    NO_REASON = "No reason in input_file"
    NO_CANCELATION_TYPE = "No cancelation_type in input_file"
    NO_DATE_SIGNATURE = "No date_signature in input_file"
    WRONG_N_ELEM = "Wrong number of elements in input_file"

    def __signature_string(self):
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
            raise VaccineManagementException(VaccinationAppointment.SIGNATURE_NOT_FOUND)
        freezer = freeze_time(
            datetime.fromtimestamp(appointment_record["_VaccinationAppointment__issued_at"]))
        freezer.start()

        # We get the issued at date timestamp from the created appointment_record
        current_date = appointment_record["_VaccinationAppointment__issued_at"]

        # We get the vaccination date timestamp from the created appointment_record
        vaccination_date = appointment_record["_VaccinationAppointment__appointment_date"]

        # Get the |days left - the timestamp| / number of days rounded
        days_left = round(abs(vaccination_date - current_date) / (24 * 60 * 60))

        appointment = cls(appointment_record["_VaccinationAppointment__patient_sys_id"],
                          appointment_record["_VaccinationAppointment__phone_number"],
                          days_left)
        freezer.stop()
        return appointment

    @classmethod
    def create_appointment_from_json_file(cls, json_file, date):
        """returns the vaccination appointment for the received input json file"""
        # Check if date is in the correct iso format
        # The easiest way is to do this is by checking ISO format, which takes into account everything
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
        days_left = round(abs(vaccination_date - current_date) / (24 * 60 * 60))

        # Instead of 10 days, the difference of the appointment days
        appointment_parser = AppointmentJsonParser(json_file)
        new_appointment = cls(
            appointment_parser.json_content[appointment_parser.PATIENT_SYSTEM_ID_KEY],
            appointment_parser.json_content[appointment_parser.CONTACT_PHONE_NUMBER_KEY],
            days_left)
        return new_appointment

    # HABRA QUE CAMBIARLO DE LADO!!! - DEMASIADA COSA, REFACTOR
    @classmethod
    def cancel_appointment_from_json_file(cls, input_file):
        """returns date_signature of the cancelled appointment"""
        from uc3m_care import JSON_FILES_PATH
        appointment_file = JSON_FILES_PATH + "store_date.json"
        vaccination_file = JSON_FILES_PATH + "store_vaccine.json"
        cancellation_file = JSON_FILES_PATH + "store_cancellation.json"

        # MOVER ESTO DONDE LOS REGEX - Atributes
        # ESTO LO HACE EL PARSER!!!!!!!!!

        # We open the input_file - get date signature
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

        # We check that date_signature type is sha256 - 64 bytes hexadecimal
        # ESTO DEBERIA IR DONDE LOS ATTRIBUTES, ES UN REGEX
        try:
            sha256_regex = r"^[a-fA-F0-9]{64}$"
            res = re.fullmatch(sha256_regex, date_signature)
            if not res:
                raise VaccineManagementException("Invalid date_signature")
        except TypeError as ex:
            raise VaccineManagementException("Invalid date_signature: not a string") from ex

        # We check that cancellation type is either Temporal or final
        try:
            cancellation_type_regex = r"Final|Temporal"
            res = re.fullmatch(cancellation_type_regex, cancellation_type)
            if not res:
                raise VaccineManagementException("Invalid cancelation_type")
        except TypeError as ex:
            raise VaccineManagementException("Invalid cancelation_type: not a string") from ex

        # We check that reason string has between 2 and 100 characters
        # We also check that it is a string
        try:
            reason_regex = r"^[\d\w\s]{2,100}$"
            res = re.fullmatch(reason_regex, reason)
            if not res:
                raise VaccineManagementException("Invalid reason")
        except TypeError as ex:
            raise VaccineManagementException("Invalid reason: not a string") from ex

        """00000000000000000000000000000000000000000000000000000000000000000000000000000000000"""
        # APPOINTMENT
        # We open the store_date.json file w/ the appointments
        try:
            with open(appointment_file, "r", encoding="utf-8", newline="") as appoint_file:
                appoint_file = json.load(appoint_file)
        except FileNotFoundError as ex:
            raise VaccineManagementException("The appointment_file received does not exist") from ex
        except json.JSONDecodeError as ex:
            raise VaccineManagementException(VaccinationAppointment.JEDWJF) from ex

        """00000000000000000000000000000000000000000000000000000000000000000000000000000000000"""
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
            raise VaccineManagementException("The appointment received does not exist")

        # Get the actual timestamp (for operation reasons) - frozen specified by each test
        current_date = datetime.now().timestamp()

        # TENGO QUE HACER QUE ESTO FUNCIONE BIEN (COMPROBACIONES)
        # Check if appointment date received has already passed
        # NO SE SI DEBERIA SER < O <= POR COMO LO DICE EL ENUNCIADO
        if datetime.fromtimestamp(
                appoint_file[appointment_index]["_VaccinationAppointment__appointment_date"]) \
                .date() < datetime.fromtimestamp(current_date).date():
            raise VaccineManagementException("The appointment date received has already passed")

        """00000000000000000000000000000000000000000000000000000000000000000000000000000000000"""
        # Vaccination log
        # We open the store_vaccine.json file and check if date_signature already vaccinated
        try:
            with open(vaccination_file, "r", encoding="utf-8", newline="") as vaccine_file:
                vaccine_file = json.load(vaccine_file)
        except FileNotFoundError as ex:
            raise VaccineManagementException("The vaccination_store does not exist") from ex
        except json.JSONDecodeError as ex:
            raise VaccineManagementException(VaccinationAppointment.JEDWJF) from ex

        # We search for a vaccination with the given date_signature
        for i in range(len(vaccine_file)):
            if vaccine_file[i]["_VaccinationLog__date_signature"] == date_signature:
                raise VaccineManagementException("Vaccine has already been administered")
            continue

        """00000000000000000000000000000000000000000000000000000000000000000000000000000000000"""
        # store_cancellation
        # We open the store_cancellation.json file and check if date_signature already
        try:
            with open(cancellation_file, "r", encoding="utf-8", newline="") as cancel_file:
                cancel_file = json.load(cancel_file)
        except FileNotFoundError as ex:
            raise VaccineManagementException("The cancellation_file does not exist") from ex
        except json.JSONDecodeError as ex:
            raise VaccineManagementException(VaccinationAppointment.JEDWJF) from ex

        # We search for a cancellation with the given date_signature
        for i in range(len(cancel_file)):
            if cancel_file[i]["date_signature"] == date_signature:
                raise VaccineManagementException("Appointment has already been canceled")
            continue

        """00000000000000000000000000000000000000000000000000000000000000000000000000000000000"""
        """00000000000000000000000000000000000000000000000000000000000000000000000000000000000"""
        # After checking everything, we will cancel the given appointment
        # In order to cancel it, we will paste the cancellation input_file into store_cancellation
        # We won't erase the store_date.json appointment, as the appointment could be reactivated

        try:
            with open(input_file, "r", encoding="utf-8", newline="") as in_file, \
                    open(cancellation_file, "r+", encoding="utf-8", newline="") as cancel_file:
                to_insert = json.load(in_file)
                destination = json.load(cancel_file)
                destination.append(to_insert)
                # set position at offset
                cancel_file.seek(0)
                # back to json
                json.dump(destination, cancel_file, indent=2)
        except Exception as ex:
            raise VaccineManagementException("Error when cancelling the appointment") from ex

        # After all the checks and creation of the cancellation, return date_signature
        return date_signature

    def is_valid_today(self):
        """returns true if today is the appointment's date"""
        today = datetime.today().date()
        date_patient = datetime.fromtimestamp(self.appointment_date).date()
        if date_patient != today:
            raise VaccineManagementException("Today is not the date")
        return True

    def register_vaccination(self):
        """register the vaccine administration"""
        if self.is_valid_today():
            vaccination_log_entry = VaccinationLog(self.date_signature)
            vaccination_log_entry.save_log_entry()
        return True
