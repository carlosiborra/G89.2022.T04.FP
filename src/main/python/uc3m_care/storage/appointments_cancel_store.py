"""Subclass of JsonStore for managing the Appointments"""

import json

from uc3m_care.storage.json_store import JsonStore
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException

from uc3m_care.data.cancelation_messages import CancelationMessage


class AppointmentsCancelStore:
    """Implements the singleton pattern"""

    # pylint: disable=invalid-name
    class __AppointmentsCancelStore(JsonStore):
        """Subclass of JsonStore for managing the Appointments"""
        _FILE_PATH = JSON_FILES_PATH + "store_cancellation.json"
        _ID_FIELD = "date_signature"
        ERROR_INVALID_APPOINTMENT_OBJECT = CancelationMessage.ERROR_INVALID_APPOINTMENT_OBJECT
        ERROR_CANCELING_APPOINTMENT = CancelationMessage.ERROR_CANCELING_APPOINTMENT

        def add_item(self, item):
            """Overrides the add_item method to verify the item to be stored"""
            # pylint: disable=import-outside-toplevel, cyclic-import
            from uc3m_care.data.vaccination_appointment import VaccinationAppointment
            if not isinstance(item, VaccinationAppointment):
                raise VaccineManagementException(self.ERROR_INVALID_APPOINTMENT_OBJECT)
            super().add_item(item)

        # In order to cancel it, we will paste the cancellation input_file into store_cancellation
        # We won't erase the store_date.json appointment, as the appointment could be reactivated
        @staticmethod
        def add_item_to_cancel_store(input_file):
            """new store static function which cancels an input file"""
            cancellation_file = JSON_FILES_PATH + "store_cancellation.json"
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
                raise VaccineManagementException(
                    AppointmentsCancelStore.ERROR_CANCELING_APPOINTMENT) from ex

    instance = None

    def __new__(cls):
        if not AppointmentsCancelStore.instance:
            AppointmentsCancelStore.instance = AppointmentsCancelStore.__AppointmentsCancelStore()
        return AppointmentsCancelStore.instance

    def __getattr__(self, nombre):
        return getattr(self.instance, nombre)

    def __setattr__(self, nombre, valor):
        return setattr(self.instance, nombre, valor)
