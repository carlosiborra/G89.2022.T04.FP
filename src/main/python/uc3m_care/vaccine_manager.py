"""Module """
import json
import re
from datetime import datetime
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
            vaccination_file = JSON_FILES_PATH + "store_vaccine.json"
            cancellation_file = JSON_FILES_PATH + "store_cancellation.json"

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

            """00000000000000000000000000000000000000000000000000000000000000000000000000000000000"""
            # APPOINTMENT
            # We open the store_date.json file w/ the appointments
            try:
                with open(appointment_file, "r", encoding="utf-8", newline="") as appoint_file:
                    appoint_file = json.load(appoint_file)
            except FileNotFoundError as ex:
                raise VaccineManagementException("The appointment received does not exist") from ex
            except json.JSONDecodeError as ex:
                raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from ex

            """00000000000000000000000000000000000000000000000000000000000000000000000000000000000"""
            # We search for an appointment with the given date_signature
            appointment_found = False
            for i in range(len(appoint_file)):
                if appoint_file[i]["_VaccinationAppointment__date_signature"] == date_signature:
                    print("found appointment", i)
                    print(len(appoint_file))
                    appointment_index = i
                    appointment_found = True
                    break
                print("Not found appointment", i)
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
                raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from ex

            # We search for a vaccination with the given date_signature
            for i in range(len(vaccine_file)):
                if vaccine_file[i]["_VaccinationLog__date_signature"] == date_signature:
                    print(len(vaccine_file))
                    print("found vaccine", i)
                    raise VaccineManagementException("Vaccine has already been administered")
                print("Not found vaccine", i)
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
                raise VaccineManagementException("JSON Decode Error - Wrong JSON Format") from ex

            # We search for a cancellation with the given date_signature
            for i in range(len(cancel_file)):
                if cancel_file[i]["date_signature"] == date_signature:
                    print(len(cancel_file))
                    print("found cancellation", i)
                    raise VaccineManagementException("Appointment has already been canceled")
                print("Not found cancellation", i)
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

            return date_signature

    instance = None

    def __new__(cls):
        if not VaccineManager.instance:
            VaccineManager.instance = VaccineManager.__VaccineManager()
        return VaccineManager.instance

    def __getattr__(self, nombre):
        return getattr(self.instance, nombre)

    def __setattr__(self, nombre, valor):
        return setattr(self.instance, nombre, valor)
