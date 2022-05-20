"""Tests for cancel_appointment method"""

import unittest

from freezegun import freeze_time
from uc3m_care import JSON_FILES_PATH, JSON_FILES_RF2_PATH, JSON_FILES_CANCELLATION
from uc3m_care import AppointmentsJsonStore
from uc3m_care import VaccineManager
from uc3m_care import PatientsJsonStore

param_list_ok = [("test_cancellation_ecv1.json", "test_1")]

param_list_nok = []


class TestRequestVacID(unittest.TestCase):
    """Class for testing request_vaccination_id"""

    @freeze_time("2022-03-08")
    def test_valid_cancellation(self):
        """ test for valid cancel_appointment test"""
        my_manager = VaccineManager()
        input_file = JSON_FILES_CANCELLATION + "test_cancellation_temporal_ecv1.json"
        file_appointment = JSON_FILES_RF2_PATH + "test_ok.json"


        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        # FAltan para poder hacer el singleton pattern!!

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        # Fixed Date in ISO format for testing purposes
        date = "2022-03-18"

        # Create an appointment for the given patient
        my_manager.get_vaccine_date(file_appointment, "2022-03-19")
        my_manager.get_vaccine_date(file_appointment, date)
        # date signature: 5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c
        # check the method
        value = my_manager.cancel_appointment(input_file)
        self.assertEqual(value,
                         "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")

        # check store_date
        # POL!! AQUI SE TIENE QUE HACER LO DE SINGLETON PATTERN EN FOLDER STORAGE - CREAR NEW _STORE


if __name__ == '__main__':
    unittest.main()
