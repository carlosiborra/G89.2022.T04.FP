"""Tests for cancel_appointment method"""

import unittest
from freezegun import freeze_time
from uc3m_care import JSON_FILES_RF2_PATH, JSON_FILES_CANCELLATION
from uc3m_care import AppointmentsJsonStore
from uc3m_care import VaccineManager
from uc3m_care import PatientsJsonStore
from uc3m_care import AppointmentsCancelStore
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
    ("json_invalid_node1_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node1_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node2_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node2_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node3_deleted.json", "Wrong number of elements in input_file"),
    ("json_invalid_node3_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node4_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node4_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node5_modified.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node6_modified.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node7_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node7_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node8_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node8_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node9_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node9_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node10_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node10_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node11_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node11_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node12_modified.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node13_modified.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node14_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node14_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node15_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node15_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node16_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node16_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node17_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node17_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node18_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node18_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node19_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node19_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node20_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node20_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node21_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node21_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node22_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node22_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node23_modified.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node24_modified.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node25_modified.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node26_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node26_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node27_deleted.json", "No date_signature in input_file"),
    ("json_invalid_node27_duplicated.json", "No date_signature in input_file"),
    ("json_invalid_node28_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node28_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node29_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node29_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node30_deleted.json", "Invalid date_signature"),
    ("json_invalid_node30_duplicated.json", "Invalid date_signature"),
    ("json_invalid_node31_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node31_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node32_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node32_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node33_deleted.json", "No cancelation_type in input_file"),
    ("json_invalid_node33_duplicated.json", "No cancelation_type in input_file"),
    ("json_invalid_node34_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node34_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node35_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node35_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node36_deleted.json", "Invalid cancelation_type"),
    ("json_invalid_node36_duplicated.json", "Invalid cancelation_type"),
    ("json_invalid_node37_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node37_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node38_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node38_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node39_deleted.json", "No reason in input_file"),
    ("json_invalid_node39_duplicated.json", "No reason in input_file"),
    ("json_invalid_node40_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node40_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node41_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node41_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node42_deleted.json", "Invalid reason"),
    ("json_invalid_node42_duplicated.json", "Invalid reason"),
    ("json_invalid_node43_deleted.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node43_duplicated.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node44_modified.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node45_modified.json", "No date_signature in input_file"),
    ("json_invalid_node46_modified.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node47_modified.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node48_modified.json", "Invalid date_signature"),
    ("json_invalid_node49_modified.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node50_modified.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node51_modified.json", "No cancelation_type in input_file"),
    ("json_invalid_node52_modified.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node53_modified.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node54_modified.json", "Invalid cancelation_type"),
    ("json_invalid_node55_modified.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node56_modified.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node57_modified.json", "No reason in input_file"),
    ("json_invalid_node58_modified.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node59_modified.json", "JSON Decode Error - Wrong JSON Format"),
    ("json_invalid_node60_modified.json", "Invalid reason"),
    ("json_invalid_node61_modified.json", "JSON Decode Error - Wrong JSON Format")]

param_list_valid_sa = [
    ("json_valid.json", "230db695dfb51529e5210244929c3bd61f203d32da20adeaf143a03a312f198f")]


# TESTS FOR EQUIVALENT CLASSES AND BOUNDARY VALUES
class TestCancelAppointmentEcBv(unittest.TestCase):
    """Class for testing cancel_appointment EC/BV"""

    @freeze_time("2022-03-08")
    def test_parametrized_valid_ec_bv_cancellation_appointment(self):
        """Parametrized tests: valid cases"""
        my_manager = VaccineManager()
        file_appointment = JSON_FILES_RF2_PATH + "test_ok.json"

        # Check the subtests
        for input_file, date_signature in param_list_valid_ec_bv:
            input_file = JSON_FILES_CANCELLATION + input_file

            # First, prepare my test, remove store patient
            file_store = PatientsJsonStore()
            file_store.delete_json_file()
            file_store_date = AppointmentsJsonStore()
            file_store_date.delete_json_file()

            # Empty store_cancellation.json to prevent errors
            file_store = AppointmentsCancelStore()
            file_store.empty_json_file()

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
                # check store_cancellation.json
                self.assertIsNotNone(file_store_date.find_item(value))

        # We empty store_cancellation.json to leave it clean and thus preventing future errors
        file_store = AppointmentsCancelStore()
        file_store.empty_json_file()

    @freeze_time("2022-03-08")
    def test_parametrized_not_valid_ec_bv_cancellation_appointment(self):
        """Parametrized tests: not valid cases"""
        my_manager = VaccineManager()
        file_appointment = JSON_FILES_RF2_PATH + "test_ok.json"

        # Check the subtests
        for input_file, raised_exception in param_list_not_valid_ec_bv:
            input_file = JSON_FILES_CANCELLATION + input_file

            # First, prepare my test, remove store patient
            file_store = PatientsJsonStore()
            file_store.delete_json_file()
            file_store_date = AppointmentsJsonStore()
            file_store_date.delete_json_file()

            # Empty store_cancellation.json to prevent errors
            file_store = AppointmentsCancelStore()
            file_store.empty_json_file()

            # Add a patient in the store
            my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                              "minombre tienelalongitudmaxima",
                                              "Regular", "+34123456789", "6")

            # Fixed Date in ISO format for testing purposes
            # Create an appointment for the given patient
            my_manager.get_vaccine_date(file_appointment, "2022-03-19")
            # In order to test with two appointments (works):
            # my_manager.get_vaccine_date(file_appointment, "2022-03-18")

            # Store the state of store store_cancellation.json
            hash_original = file_store_date.data_hash()
            # Check raised exceptions - TEST
            with self.subTest(test=input_file):
                with self.assertRaises(VaccineManagementException) as c_m:
                    my_manager.cancel_appointment(input_file)
                self.assertEqual(c_m.exception.message, raised_exception)
                # Read the file again to compare
                hash_new = file_store_date.data_hash()
                self.assertEqual(hash_new, hash_original)
            # We do not empty store_cancellation.json as we have checked through the hashes
            # that is the same file as the original store_cancellation.json received

    @freeze_time("2022-03-08")
    def test_specific_not_valid_ec_bv_encv6_cancellation_appointment(self):
        """Specific tests: not valid test for test_date_signature_ecnv6.json"""
        my_manager = VaccineManager()
        input_file = JSON_FILES_CANCELLATION + "test_date_signature_ecnv6.json"
        file_appointment = JSON_FILES_RF2_PATH + "test_ok.json"

        # First, prepare my test, remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()

        # Clean the content of previous store_cancellation.json
        file_store = AppointmentsCancelStore()
        file_store.empty_json_file()
        hash_original = file_store_date.data_hash()

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
            # Read the file again to compare
            hash_new = file_store_date.data_hash()
            self.assertEqual(hash_new, hash_original)
        # We do not empty store_cancellation.json as we have checked through the hashes
        # that is the same file as the original store_cancellation.json received

    @freeze_time("2022-03-08")
    def test_specific_not_valid_ec_bv_encv7_cancellation_appointment(self):
        """Specific tests: not valid test for test_date_signature_ecnv7.json"""
        my_manager = VaccineManager()
        input_file = JSON_FILES_CANCELLATION + "test_date_signature_ecnv7.json"
        file_appointment = JSON_FILES_RF2_PATH + "test_ok.json"

        # First, prepare my test, remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()

        # Clean the content of previous store_cancellation.json
        file_store = AppointmentsCancelStore()
        file_store.empty_json_file()

        # Add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        # Create an appointment for the given patient
        # json date signature: 5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c
        my_manager.get_vaccine_date(file_appointment, "2022-03-19")
        my_manager.get_vaccine_date(file_appointment, "2022-03-18")

        # Store the state of store store_cancellation.json
        hash_original = file_store_date.data_hash()
        # Check raised exception - TEST
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(input_file)
        self.assertEqual(c_m.exception.message, "Vaccine has already been administered")

        # Read the file again to compare
        hash_new = file_store_date.data_hash()
        self.assertEqual(hash_new, hash_original)
        # We do not empty store_cancellation.json as we have checked through the hashes
        # that is the same file as the original store_cancellation.json received

    @freeze_time("2022-03-08")
    def test_specific_not_valid_ec_bv_encv8_cancellation_appointment(self):
        """Specific tests: not valid test for test_date_signature_ecnv8.json"""
        my_manager = VaccineManager()
        input_file = JSON_FILES_CANCELLATION + "test_date_signature_ecnv8.json"
        file_appointment = JSON_FILES_RF2_PATH + "test_ok.json"

        # First, prepare my test, remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()

        # Clean the content of previous store_cancellation.json
        file_store = AppointmentsCancelStore()
        file_store.empty_json_file()

        # Add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        # Create an appointment for the given patient
        my_manager.get_vaccine_date(file_appointment, "2022-03-19")

        # Cancel the appointment
        my_manager.cancel_appointment(input_file)

        # Store the state of store store_cancellation.json
        hash_original = file_store_date.data_hash()
        # Now we re-cancel the appointment
        # Check raised exception - TEST
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(input_file)
        self.assertEqual(c_m.exception.message,
                         "Appointment has already been canceled")

        # Read the file again to compare
        hash_new = file_store_date.data_hash()
        self.assertEqual(hash_new, hash_original)
        # We do not empty store_cancellation.json as we have checked through the hashes
        # that is the same file as the original store_cancellation.json received


# TESTS FOR THE SYNTAX ANALYSIS
class TestCancelAppointmentSyntaxAnalysis(unittest.TestCase):
    """Class for testing cancel_appointment syntax analysis"""

    @freeze_time("2022-03-08")
    def test_parametrized_valid_sa_cancellation_appointment(self):
        """Parametrized tests: valid case of syntax analysis"""
        my_manager = VaccineManager()
        file_appointment = JSON_FILES_RF2_PATH + "test_ok.json"

        # Check the subtests
        for input_file, date_signature in param_list_valid_sa:
            input_file = JSON_FILES_CANCELLATION + input_file

            # First, prepare my test, remove store patient
            file_store = PatientsJsonStore()
            file_store.delete_json_file()
            file_store_date = AppointmentsJsonStore()
            file_store_date.delete_json_file()

            # Empty store_cancellation.json to prevent errors
            file_store = AppointmentsCancelStore()
            file_store.empty_json_file()

            # Add a patient in the store
            my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                              "minombre tienelalongitudmaxima",
                                              "Regular", "+34123456789", "6")

            # Fixed Date in ISO format for testing purposes
            # Create an appointment for the given patient
            my_manager.get_vaccine_date(file_appointment, "2022-03-19")

            # Check returned date_signature - TEST
            with self.subTest(test=input_file):
                value = my_manager.cancel_appointment(input_file)
                self.assertEqual(value, date_signature)
                # check store_cancellation.json
                self.assertIsNotNone(file_store_date.find_item(value))

        # We empty store_cancellation.json to leave it clean and thus preventing future errors
        file_store = AppointmentsCancelStore()
        file_store.empty_json_file()

    @freeze_time("2022-03-08")
    def test_parametrized_not_valid_sa_cancellation_appointment(self):
        """Parametrized tests: not valid cases of syntax analysis"""
        my_manager = VaccineManager()
        file_appointment = JSON_FILES_RF2_PATH + "test_ok.json"

        # Check the subtests
        for input_file, raised_exception in param_list_not_valid_sa:
            input_file = JSON_FILES_CANCELLATION + input_file

            # First, prepare my test, remove store patient
            file_store = PatientsJsonStore()
            file_store.delete_json_file()
            file_store_date = AppointmentsJsonStore()
            file_store_date.delete_json_file()

            # Empty store_cancellation.json to prevent errors
            file_store = AppointmentsCancelStore()
            file_store.empty_json_file()

            # Add a patient in the store
            my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                              "minombre tienelalongitudmaxima",
                                              "Regular", "+34123456789", "6")

            # Store the state of store store_cancellation.json
            hash_original = file_store_date.data_hash()
            # Fixed Date in ISO format for testing purposes
            # Create an appointment for the given patient
            my_manager.get_vaccine_date(file_appointment, "2022-03-19")

            # Check raised exceptions - TEST
            with self.subTest(test=input_file):
                with self.assertRaises(VaccineManagementException) as c_m:
                    my_manager.cancel_appointment(input_file)
                self.assertEqual(c_m.exception.message, raised_exception)

            # Read the file again to compare
            hash_new = file_store_date.data_hash()
            self.assertEqual(hash_new, hash_original)
            # We do not empty store_cancellation.json as we have checked through the hashes
            # that is the same file as the original store_cancellation.json received


# TESTS FOR NON TESTED EXCEPTIONS
class TestExtraNonTested(unittest.TestCase):
    """Tests for specific exceptions not tested before"""

    @freeze_time("2022-03-08")
    def test_input_file_not_found(self):
        """Test when input file is not found"""
        my_manager = VaccineManager()
        input_file = JSON_FILES_CANCELLATION + "invented.json"
        file_appointment = JSON_FILES_RF2_PATH + "test_ok.json"

        # First, prepare my test, remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()

        # Clean the content of previous store_cancellation.json
        file_store = AppointmentsCancelStore()
        file_store.empty_json_file()

        # Add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        # Create an appointment for the given patient
        my_manager.get_vaccine_date(file_appointment, "2022-03-19")

        # Store the state of store store_cancellation.json
        hash_original = file_store_date.data_hash()
        # Check raised exception - TEST
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(input_file)
        self.assertEqual(c_m.exception.message,
                         "File is not found")

        # Read the file again to compare
        hash_new = file_store_date.data_hash()
        self.assertEqual(hash_new, hash_original)
        # We do not empty store_cancellation.json as we have checked through the hashes
        # that is the same file as the original store_cancellation.json received

    @freeze_time("2022-03-08")
    def test_input_file_not_json(self):
        """Test when input file is not json"""
        my_manager = VaccineManager()
        input_file = JSON_FILES_CANCELLATION + "invented"
        file_appointment = JSON_FILES_RF2_PATH + "test_ok.json"

        # First, prepare my test, remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()

        # Clean the content of previous store_cancellation.json
        file_store = AppointmentsCancelStore()
        file_store.empty_json_file()

        # Add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        # Create an appointment for the given patient
        my_manager.get_vaccine_date(file_appointment, "2022-03-19")

        # Store the state of store store_cancellation.json
        hash_original = file_store_date.data_hash()
        # Check raised exception - TEST
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(input_file)
        self.assertEqual(c_m.exception.message,
                         "File is not found")

        # Read the file again to compare
        hash_new = file_store_date.data_hash()
        self.assertEqual(hash_new, hash_original)
        # We do not empty store_cancellation.json as we have checked through the hashes
        # that is the same file as the original store_cancellation.json received

    @freeze_time("2022-03-08")
    def test_appointment_file_not_found(self):
        """Test when appointment file is not found"""
        my_manager = VaccineManager()
        input_file = JSON_FILES_CANCELLATION + "json_valid.json"
        file_appointment = JSON_FILES_RF2_PATH + "nofile.json"

        # First, prepare my test, remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()

        # Clean the content of previous store_cancellation.json
        file_store = AppointmentsCancelStore()
        file_store.empty_json_file()

        # Add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        # Store the state of store store_cancellation.json
        hash_original = file_store_date.data_hash()
        # Check raised exception - TEST
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.get_vaccine_date(file_appointment, "2022-03-19")
            my_manager.cancel_appointment(input_file)
        self.assertEqual(c_m.exception.message,
                         "File is not found")

        # Read the file again to compare
        hash_new = file_store_date.data_hash()
        self.assertEqual(hash_new, hash_original)
        # We do not empty store_cancellation.json as we have checked through the hashes
        # that is the same file as the original store_cancellation.json received

    @freeze_time("2022-03-08")
    def test_appointment_file_not_json(self):
        """Test when appointment file is not json"""
        my_manager = VaccineManager()
        input_file = JSON_FILES_CANCELLATION + "json_valid.json"
        file_appointment = JSON_FILES_RF2_PATH + "nofile"

        # First, prepare my test, remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()

        # Clean the content of previous store_cancellation.json
        file_store = AppointmentsCancelStore()
        file_store.empty_json_file()

        # Add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        # Store the state of store store_cancellation.json
        hash_original = file_store_date.data_hash()
        # Check raised exception - TEST
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.get_vaccine_date(file_appointment, "2022-03-19")
            my_manager.cancel_appointment(input_file)
        self.assertEqual(c_m.exception.message,
                         "File is not found")

        # Read the file again to compare
        hash_new = file_store_date.data_hash()
        self.assertEqual(hash_new, hash_original)
        # We do not empty store_cancellation.json as we have checked through the hashes
        # that is the same file as the original store_cancellation.json received


if __name__ == '__main__':
    unittest.main()
