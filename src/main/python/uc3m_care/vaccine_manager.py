"""Module """
import json
import re
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.data.vaccination_appointment import VaccinationAppointment
from uc3m_care import JSON_FILES_PATH, JSON_FILES_CANCELLATION


class VaccineManager:
    """Class for providing the methods for managing the vaccination process"""

    # pylint: disable=invalid-name
    class __VaccineManager:
        def __init__(self):
            pass

        # pylint: disable=too-many-arguments
        # pylint: disable=no-self-use
        def request_vaccination_id(self, patient_id,
                                   name_surname,
                                   registration_type,
                                   phone_number,
                                   age):
            """Register the patinent into the patients file"""
            my_patient = VaccinePatientRegister(patient_id,
                                                name_surname,
                                                registration_type,
                                                phone_number,
                                                age)

            my_patient.save_patient()
            return my_patient.patient_sys_id

        def get_vaccine_date(self, input_file, date):
            """Gets an appointment for a registered patient: json file, date in ISO format"""
            my_sign = VaccinationAppointment.create_appointment_from_json_file(input_file, date)
            # save the date in store_date.json
            my_sign.save_appointment()
            return my_sign.date_signature

        def vaccine_patient(self, date_signature):
            """Register the vaccination of the patient"""
            appointment = VaccinationAppointment.get_appointment_from_date_signature(date_signature)
            return appointment.register_vaccination()

        # HABRA QUE CAMBIARLO DE LADO!!! - DEMASIADA COSA, REFACTOR

        def cancel_appointment(self, input_file):
            """Deletes an appointment from json file"""
            appointment_file = JSON_FILES_PATH + "store_date.json"

            # MOVER ESTO DONDE LOS REGEX - Atributes
            # ESTO LO HACE EL PARSER!!!!!!!!!

            # We open the input_file - get date signature
            try:
                with open(input_file, "r", encoding="utf-8", newline="") as file:
                    file = json.load(file)
            except FileNotFoundError as ex:
                raise VaccineManagementException("File is not found") from ex
            except json.JSONDecodeError as ex:
                raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from ex

            # Check if date_signature exists in input file and save its value
            try:
                date_signature = file["date_signature"]
            except Exception as ex:
                raise VaccineManagementException("No date_signature in input_file") from ex

            # Check if cancelation_type exists in input file
            try:
                file["cancelation_type"]
            except Exception as ex:
                raise VaccineManagementException("No cancelation_type in input_file") from ex

            # Check if reason exists in input file
            try:
                file["reason"]
            except Exception as ex:
                raise VaccineManagementException("No reason in input_file") from ex

            # We check that date_signature type is sha256 - 64 bytes hexadecimal
            # ESTO DEBERIA IR DONDE LOS ATTRIBUTES, ES UN REGEX
            sha256_regex = r"^[a-fA-F0-9]{64}$"
            res = re.fullmatch(sha256_regex, date_signature)
            if not res:
                raise VaccineManagementException("Wrong date_signature")

            # We check that cancellation type is either Temporal or final
            if file["cancelation_type"] not in ["Temporal", "Final"]:
                raise VaccineManagementException("Wrong cancelation_type value")

            # We check that reason string has between 2 and 100 characters
            # We also check that it is a string
            try:
                if len(file["reason"]) < 2 or len(file["reason"]) > 100:
                    raise VaccineManagementException("Wrong reason length")
            except TypeError as ty:
                raise VaccineManagementException("Wrong reason type") from ty

            # APPOINTMENT
            # We open the store_date.json file w/ the appointments
            try:
                with open(appointment_file, "r", encoding="utf-8", newline="") as appoint_file:
                    appoint_file = json.load(appoint_file)
            except FileNotFoundError as ex:
                raise VaccineManagementException("The appointment received does not exist") from ex
            except json.JSONDecodeError as ex:
                raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from ex

            # We search for an appointment with the given date_signature
            for i in range(len(appoint_file)):
                if appoint_file[i]["_VaccinationAppointment__date_signature"] == date_signature:
                    print("found", i)
                    return date_signature
                print("Not found", i)
                continue
            raise VaccineManagementException("Error accessing the appointment received")


    instance = None

    def __new__(cls):
        if not VaccineManager.instance:
            VaccineManager.instance = VaccineManager.__VaccineManager()
        return VaccineManager.instance

    def __getattr__(self, nombre):
        return getattr(self.instance, nombre)

    def __setattr__(self, nombre, valor):
        return setattr(self.instance, nombre, valor)
