"""Tests for cancel_appointment method"""

import unittest
import json
from freezegun import freeze_time
from uc3m_care import JSON_FILES_PATH, JSON_FILES_RF2_PATH, JSON_FILES_CANCELLATION
from uc3m_care import AppointmentsJsonStore
from uc3m_care import VaccineManager
from uc3m_care import PatientsJsonStore
from uc3m_care import VaccineManagementException

param_list_ok = [("test_cancellation_ecv1.json", "test_1")]

param_list_nok = []


class TestCancelAppointment(unittest.TestCase):
    """Class for testing cancel_appointment"""

    @freeze_time("2022-03-08")
    def test_valid_cancellation_temporal(self):
        """ test for valid cancel_appointment test"""
        print("valid")
        my_manager = VaccineManager()
        input_file = JSON_FILES_CANCELLATION + "test_cancellation_temporal_ecv1.json"
        file_appointment = JSON_FILES_RF2_PATH + "test_ok.json"
        store_cancellation = JSON_FILES_PATH + "store_cancellation.json"

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        # remove the content of previous store_cancellation.json
        # FAltan para poder hacer el singleton pattern!!!!!!!
        # Se tendría que hacer con el singleton pattern en la parte de storage y data (+attr)

        with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
            f.close()
        brackets = []
        with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
            json.dump(brackets, f)

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        # Fixed Date in ISO format for testing purposes
        date = "2022-03-18"

        # Create an appointment for the given patient
        my_manager.get_vaccine_date(file_appointment, "2022-03-19")
        my_manager.get_vaccine_date(file_appointment, date)
        # date signature: 230db695dfb51529e5210244929c3bd61f203d32da20adeaf143a03a312f198f
        # check the method
        value = my_manager.cancel_appointment(input_file)
        self.assertEqual(value,
                         "230db695dfb51529e5210244929c3bd61f203d32da20adeaf143a03a312f198f")

    @freeze_time("2022-03-08")
    def test_non_valid_cancellation_temporal(self):
        """ test for valid cancel_appointment test"""
        print("invalid")
        my_manager = VaccineManager()
        input_file = JSON_FILES_CANCELLATION + "test_cancellation_temporal_ecnv1.json"
        file_appointment = JSON_FILES_RF2_PATH + "test_ok.json"
        store_cancellation = JSON_FILES_PATH + "store_cancellation.json"

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        # remove the content of previous store_cancellation.json
        # Se tendría que hacer con el singleton pattern en la parte de storage y data (+attr)
        # FAltan para poder hacer el singleton pattern!!!!!!!
        with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
            f.close()
        brackets = []
        with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
            json.dump(brackets, f)

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
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(input_file)
        self.assertEqual(c_m.exception.message, "Vaccine has already been administered")

        # check store_date
        # POL!! AQUI SE TIENE QUE HACER LO DE SINGLETON PATTERN EN FOLDER STORAGE - CREAR NEW _STORE


if __name__ == '__main__':
    unittest.main()
