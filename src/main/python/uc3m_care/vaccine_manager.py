"""Module """
import json
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

        #pylint: disable=too-many-arguments
        # pylint: disable=no-self-use
        def request_vaccination_id (self, patient_id,
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

        def get_vaccine_date (self, input_file, date):
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
            date_signature = file["date_signature"]

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
            raise VaccineManagementException("The appointment received does not exist")
    instance = None

    def __new__(cls):
        if not VaccineManager.instance:
            VaccineManager.instance = VaccineManager.__VaccineManager()
        return VaccineManager.instance

    def __getattr__(self, nombre):
        return getattr(self.instance, nombre)

    def __setattr__(self, nombre, valor):
        return setattr(self.instance, nombre, valor)
