"""Tests for cancel_appointment method"""

import unittest
import json
from freezegun import freeze_time
from uc3m_care import JSON_FILES_PATH, JSON_FILES_RF2_PATH, JSON_FILES_CANCELLATION
from uc3m_care import AppointmentsJsonStore
from uc3m_care import VaccineManager
from uc3m_care import PatientsJsonStore
from uc3m_care import VaccineManagementException

param_list_valid_ec_bv = [
    ("test_cancelation_type_ecv1.json",
     "230db695dfb51529e5210244929c3bd61f203d32da20adeaf143a03a312f198f"),
    ("test_cancelation_type_ecv2.json",
     "230db695dfb51529e5210244929c3bd61f203d32da20adeaf143a03a312f198f"),
    ("test_date_signature_ecv1.json",
     "230db695dfb51529e5210244929c3bd61f203d32da20adeaf143a03a312f198f"),
    ("test_reason_ecv1.json",
     "230db695dfb51529e5210244929c3bd61f203d32da20adeaf143a03a312f198f"),
    ("test_reason_ecv2.json",
     "230db695dfb51529e5210244929c3bd61f203d32da20adeaf143a03a312f198f"),
    ("test_reason_ecv3.json",
     "230db695dfb51529e5210244929c3bd61f203d32da20adeaf143a03a312f198f"),
    ("test_reason_ecv4.json",
     "230db695dfb51529e5210244929c3bd61f203d32da20adeaf143a03a312f198f")]

param_list_not_valid_ec_bv = [
    ("test_cancelation_type_ecnv1.json", "Invalid cancelation_type"),
    ("test_cancelation_type_ecnv2.json", "Invalid cancelation_type: not a string"),
    ("test_date_signature_ecnv1.json", "Invalid date_signature"),
    ("test_date_signature_ecnv2.json", "Invalid date_signature"),
    ("test_date_signature_ecnv3.json", "Invalid date_signature"),
    ("test_date_signature_ecnv4.json", "Invalid date_signature: not a string"),
    ("test_date_signature_ecnv5.json", "The appointment received does not exist"),
    ("test_reason_ecnv1.json", "Invalid reason"),
    ("test_reason_ecnv2.json", "Invalid reason"),
    ("test_reason_ecnv3.json", "Invalid reason: not a string")]

param_list_not_valid_sa = [
    ("json_invalid_node1_deleted.json", "JSON Decode Error - Wrong JSON Format")]

# NOTA: HACE FALTA:
# Se tendría que hacer con el REFACTOR en la parte de storage y data (+attr)
# file_store_date = AppointmentsJsonStore() PERO CON CANCELLATION AL PREPARAR LOS TESTS

# TESTS FOR EQUIVALENT CLASSES AND BOUNDARY VALUES


class TestCancelAppointmentEcBv(unittest.TestCase):
    """Class for testing cancel_appointment EC/BV"""

    @freeze_time("2022-03-08")
    def test_parametrized_valid_ec_bv_cancellation_appointment(self):
        """Parametrized tests: valid cases F1"""
        my_manager = VaccineManager()
        file_appointment = JSON_FILES_RF2_PATH + "test_ok.json"
        store_cancellation = JSON_FILES_PATH + "store_cancellation.json"

        # Check the subtests
        for input_file, date_signature in param_list_valid_ec_bv:
            input_file = JSON_FILES_CANCELLATION + input_file

            # First, prepare my test, remove store patient
            file_store = PatientsJsonStore()
            file_store.delete_json_file()
            file_store_date = AppointmentsJsonStore()
            file_store_date.delete_json_file()

            # Empty store_cancellation.json to prevent errors
            with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
                f.close()
            brackets = []
            with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
                json.dump(brackets, f)

            # Add a patient in the store
            my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                              "minombre tienelalongitudmaxima",
                                              "Regular", "+34123456789", "6")

            # Fixed Date in ISO format for testing purposes
            # Create an appointment for the given patient
            my_manager.get_vaccine_date(file_appointment, "2022-03-19")
            # In order to test with two appointments (works):
            # my_manager.get_vaccine_date(file_appointment, "2022-03-18")

            # Check returned date_signature - TEST
            with self.subTest(test=input_file):
                value = my_manager.cancel_appointment(input_file)
                self.assertEqual(value, date_signature)

        # We empty store_cancellation.json to leave it clean and thus preventing future errors
        with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
            f.close()
        brackets = []
        with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
            json.dump(brackets, f)

    @freeze_time("2022-03-08")
    def test_parametrized_not_valid_ec_bv_cancellation_appointment(self):
        """Parametrized tests: not valid cases F1"""
        my_manager = VaccineManager()
        file_appointment = JSON_FILES_RF2_PATH + "test_ok.json"
        store_cancellation = JSON_FILES_PATH + "store_cancellation.json"

        # Check the subtests
        for input_file, raised_exception in param_list_not_valid_ec_bv:
            input_file = JSON_FILES_CANCELLATION + input_file

            # First, prepare my test, remove store patient
            file_store = PatientsJsonStore()
            file_store.delete_json_file()
            file_store_date = AppointmentsJsonStore()
            file_store_date.delete_json_file()

            # Empty store_cancellation.json to prevent errors
            with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
                f.close()
            brackets = []
            with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
                json.dump(brackets, f)

            # Add a patient in the store
            my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                              "minombre tienelalongitudmaxima",
                                              "Regular", "+34123456789", "6")

            # Fixed Date in ISO format for testing purposes
            # Create an appointment for the given patient
            my_manager.get_vaccine_date(file_appointment, "2022-03-19")
            # In order to test with two appointments (works):
            # my_manager.get_vaccine_date(file_appointment, "2022-03-18")

            # Check raised exceptions - TEST
            with self.subTest(test=input_file):
                with self.assertRaises(VaccineManagementException) as c_m:
                    my_manager.cancel_appointment(input_file)
                self.assertEqual(c_m.exception.message, raised_exception)

        # We empty store_cancellation.json to leave it clean and thus preventing future errors
        with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
            f.close()
        brackets = []
        with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
            json.dump(brackets, f)

    @freeze_time("2022-03-08")
    def test_specific_non_valid_ec_bv_encv6_cancellation_appointment(self):
        """Specific tests: not valid test for test_date_signature_ecnv6.json in F1"""
        my_manager = VaccineManager()
        input_file = JSON_FILES_CANCELLATION + "test_date_signature_ecnv6.json"
        file_appointment = JSON_FILES_RF2_PATH + "test_ok.json"
        store_cancellation = JSON_FILES_PATH + "store_cancellation.json"

        # First, prepare my test, remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()

        # Clean the content of previous store_cancellation.json
        with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
            f.close()
        brackets = []
        with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
            json.dump(brackets, f)

        # Add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        # Create an appointment for the given patient
        my_manager.get_vaccine_date(file_appointment, "2022-03-18")

        @freeze_time("2022-03-20")
        def set_diff_time():
            """With this function we change the time after the appointment date"""
            # Check raised exception - TEST
            with self.assertRaises(VaccineManagementException) as c_m:
                my_manager.cancel_appointment(input_file)
            self.assertEqual(c_m.exception.message,
                             "The appointment date received has already passed")

        # We clean again the store_cancellation.json to prevent future errors
        with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
            f.close()
        brackets = []
        with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
            json.dump(brackets, f)

    @freeze_time("2022-03-08")
    def test_specific_non_valid_ec_bv_encv7_cancellation_appointment(self):
        """Specific tests: not valid test for test_date_signature_ecnv7.json in F1"""
        my_manager = VaccineManager()
        input_file = JSON_FILES_CANCELLATION + "test_date_signature_ecnv7.json"
        file_appointment = JSON_FILES_RF2_PATH + "test_ok.json"
        store_cancellation = JSON_FILES_PATH + "store_cancellation.json"

        # First, prepare my test, remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()

        # Clean the content of previous store_cancellation.json
        with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
            f.close()
        brackets = []
        with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
            json.dump(brackets, f)

        # Add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        # Create an appointment for the given patient
        # json date signature: 5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c
        my_manager.get_vaccine_date(file_appointment, "2022-03-19")
        my_manager.get_vaccine_date(file_appointment, "2022-03-18")

        # Check raised exception - TEST
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(input_file)
        self.assertEqual(c_m.exception.message, "Vaccine has already been administered")

        # We clean again the store_cancellation.json to prevent future errors
        with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
            f.close()
        brackets = []
        with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
            json.dump(brackets, f)

    @freeze_time("2022-03-08")
    def test_specific_non_valid_ec_bv_encv8_cancellation_appointment(self):
        """Specific tests: not valid test for test_date_signature_ecnv8.json in F1"""
        my_manager = VaccineManager()
        input_file = JSON_FILES_CANCELLATION + "test_date_signature_ecnv8.json"
        file_appointment = JSON_FILES_RF2_PATH + "test_ok.json"
        store_cancellation = JSON_FILES_PATH + "store_cancellation.json"

        # First, prepare my test, remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()

        # Clean the content of previous store_cancellation.json
        with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
            f.close()
        brackets = []
        with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
            json.dump(brackets, f)

        # Add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        # Create an appointment for the given patient
        my_manager.get_vaccine_date(file_appointment, "2022-03-19")

        # Cancel the appointment
        my_manager.cancel_appointment(input_file)

        # Now we re-cancel the appointment
        # Check raised exception - TEST
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(input_file)
        self.assertEqual(c_m.exception.message,
                         "Appointment has already been canceled")

        # We clean again the store_cancellation.json to prevent future errors
        with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
            f.close()
        brackets = []
        with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
            json.dump(brackets, f)


# TESTS FOR THE SYNTAX ANALYSIS


class TestCancelAppointmentSyntaxAnalysis(unittest.TestCase):
    """Class for testing cancel_appointment syntax analysis"""

    @freeze_time("2022-03-08")
    def test_parametrized_not_valid_sa_cancellation_appointment(self):
        """Parametrized tests: not valid cases F1"""
        my_manager = VaccineManager()
        file_appointment = JSON_FILES_RF2_PATH + "test_ok.json"
        store_cancellation = JSON_FILES_PATH + "store_cancellation.json"

        # Check the subtests
        for input_file, raised_exception in param_list_not_valid_sa:
            input_file = JSON_FILES_CANCELLATION + input_file

            # First, prepare my test, remove store patient
            file_store = PatientsJsonStore()
            file_store.delete_json_file()
            file_store_date = AppointmentsJsonStore()
            file_store_date.delete_json_file()

            # Empty store_cancellation.json to prevent errors
            with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
                f.close()
            brackets = []
            with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
                json.dump(brackets, f)

            # Add a patient in the store
            my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                              "minombre tienelalongitudmaxima",
                                              "Regular", "+34123456789", "6")

            # Fixed Date in ISO format for testing purposes
            # Create an appointment for the given patient
            my_manager.get_vaccine_date(file_appointment, "2022-03-19")

            # Check raised exceptions - TEST
            with self.subTest(test=input_file):
                with self.assertRaises(VaccineManagementException) as c_m:
                    my_manager.cancel_appointment(input_file)
                self.assertEqual(c_m.exception.message, raised_exception)

        # We empty store_cancellation.json to leave it clean and thus preventing future errors
        with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
            f.close()
        brackets = []
        with open(store_cancellation, "w", encoding="utf-8", newline="") as f:
            json.dump(brackets, f)


if __name__ == '__main__':
    unittest.main()
