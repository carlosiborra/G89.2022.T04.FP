"""Tests for get_vaccine_date method"""

from unittest import TestCase
import os
import shutil
from freezegun import freeze_time
from uc3m_care import VaccineManager
from uc3m_care import VaccineManagementException
from uc3m_care import JSON_FILES_PATH, JSON_FILES_RF2_PATH
from uc3m_care import AppointmentsJsonStore
from uc3m_care import PatientsJsonStore
from uc3m_care.data.attribute.attribute_phone_number import PhoneNumber
from uc3m_care.data.attribute.attribute_patient_system_id import PatientSystemId

param_list_nok = [
    ("test_dup_all.json", "2022-03-18", "JSON Decode Error - Wrong JSON Format"),
    ("test_dup_char_plus.json", "2022-03-18", PhoneNumber.PHONE_NUMBER_NOT_VALID),
    ("test_dup_colon.json", "2022-03-18", "JSON Decode Error - Wrong JSON Format"),
    ("test_dup_comillas.json", "2022-03-18", "JSON Decode Error - Wrong JSON Format"),
    ("test_dup_comma.json", "2022-03-18", "JSON Decode Error - Wrong JSON Format"),
    ("test_dup_content.json", "2022-03-18", "JSON Decode Error - Wrong JSON Format"),
    ("test_dup_data1.json", "2022-03-18", "JSON Decode Error - Wrong JSON Format"),
    ("test_dup_data1_content.json", "2022-03-18", PatientSystemId.PATIENT_ID_NOT_VALID),
    ("test_dup_data2.json", "2022-03-18", "JSON Decode Error - Wrong JSON Format"),
    ("test_dup_data2_content.json", "2022-03-18", PhoneNumber.PHONE_NUMBER_NOT_VALID),
    ("test_dup_field1.json", "2022-03-18", "JSON Decode Error - Wrong JSON Format"),
    ("test_dup_field2.json", "2022-03-18", "JSON Decode Error - Wrong JSON Format"),
    ("test_dup_final_bracket.json", "2022-03-18", "JSON Decode Error - Wrong JSON Format"),
    ("test_dup_initial_bracket.json", "2022-03-18", "JSON Decode Error - Wrong JSON Format"),
    ("test_dup_label1.json", "2022-03-18", "JSON Decode Error - Wrong JSON Format"),
    ("test_dup_label1_content.json", "2022-03-18", "Bad label patient_id"),
    ("test_dup_label2.json", "2022-03-18", "JSON Decode Error - Wrong JSON Format"),
    ("test_dup_label2_content.json", "2022-03-18", "Bad label contact phone"),
    ("test_dup_phone.json", "2022-03-18", PhoneNumber.PHONE_NUMBER_NOT_VALID),
    ("test_empty.json", "2022-03-18", "Bad label patient_id"),
    ("test_mod_char_plus.json", "2022-03-18", PhoneNumber.PHONE_NUMBER_NOT_VALID),
    ("test_mod_data1.json", "2022-03-18", PatientSystemId.PATIENT_ID_NOT_VALID),
    ("test_mod_data2.json", "2022-03-18", PhoneNumber.PHONE_NUMBER_NOT_VALID),
    ("test_mod_label1.json", "2022-03-18", "Bad label patient_id"),
    ("test_mod_label2.json", "2022-03-18", "Bad label contact phone"),
    ("test_mod_phone.json", "2022-03-18", PhoneNumber.PHONE_NUMBER_NOT_VALID),
    ("test_no_char_plus.json", "2022-03-18", PhoneNumber.PHONE_NUMBER_NOT_VALID),
    ("test_no_colon.json", "2022-03-18", "JSON Decode Error - Wrong JSON Format"),
    ("test_no_comillas.json", "2022-03-18", "JSON Decode Error - Wrong JSON Format"),
    ("test_no_phone.json", "2022-03-18", PhoneNumber.PHONE_NUMBER_NOT_VALID),
    # INVALID DATE TESTS
    ("test_ok.json", "2022-03-07", "vaccination_date equal or earlier than current_date"),
    ("test_ok.json", "2022-03-08", "vaccination_date equal or earlier than current_date"),
    ("test_ok.json", "2021-03-18", "vaccination_date equal or earlier than current_date"),
    ("test_ok.json", "2022-02-18", "vaccination_date equal or earlier than current_date"),
    ("test_ok.json", "2022-13-01", "Wrong vaccination_date format"),
    ("test_ok.json", "2022-00-04", "Wrong vaccination_date format"),
    ("test_ok.json", "2022-03-32", "Wrong vaccination_date format"),
    ("test_ok.json", "2022-04-31", "Wrong vaccination_date format"),
    ("test_ok.json", "2022-02-29", "Wrong vaccination_date format"),
    ("test_ok.json", "2024-02-30", "Wrong vaccination_date format"),
    ("test_ok.json", "2022-04-00", "Wrong vaccination_date format"),
    ("test_ok.json", "04-2022-04", "Wrong vaccination_date format"),
    ("test_ok.json", "04-04-2022", "Wrong vaccination_date format"),
    ("test_ok.json", "22-04-04", "Wrong vaccination_date format"),
    ("test_ok.json", "2022-4-04", "Wrong vaccination_date format"),
    ("test_ok.json", "2022-04-4", "Wrong vaccination_date format"),
    ("test_ok.json", "2022-4-4", "Wrong vaccination_date format"),
    ("test_ok.json", "202203-18", "Wrong vaccination_date format"),
    ("test_ok.json", "202203 18", "Wrong vaccination_date format"),
    ("test_ok.json", "2022-0318", "Wrong vaccination_date format"),
    ("test_ok.json", "2022 0318", "Wrong vaccination_date format"),
    ("test_ok.json", "2022 03 18", "Wrong vaccination_date format"),
    ("test_ok.json", "20220318", "Wrong vaccination_date format"),
    ("test_ok.json", 20221201, "Wrong vaccination_date format")]


class TestGetVaccineDate(TestCase):
    """Class for testing get_vaccine_date"""

    @freeze_time("2022-03-08")
    def test_get_vaccine_date_ok(self):
        """test ok"""
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        # Fixed Date in ISO format for testing purposes
        date = "2022-03-18"

        # check the method
        value = my_manager.get_vaccine_date(file_test, date)
        self.assertEqual(value,
                         "5a06c7bede3d584e934e2f5bd3861e625cb31937f9f1a5362a51fbbf38486f1c")
        # check store_date
        self.assertIsNotNone(file_store_date.find_item(value))

    @freeze_time("2022-03-08")
    def test_get_vaccine_date_ok_bv_1(self):
        """test ok"""
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        # Fixed Date in ISO format for testing purposes
        date = "2022-12-18"

        # check the method
        value = my_manager.get_vaccine_date(file_test, date)
        self.assertEqual(value,
                         "8f1ec866e9017e15921649419fd7ddbd1927fcb170906738e1dc3125e2d599ec")
        # check store_date
        self.assertIsNotNone(file_store_date.find_item(value))

    @freeze_time("2022-03-08")
    def test_get_vaccine_date_ok_bv_2(self):
        """test ok"""
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        # Fixed Date in ISO format for testing purposes
        date = "2023-01-18"

        # Check the method
        value = my_manager.get_vaccine_date(file_test, date)
        self.assertEqual(value,
                         "1b0887bf18529ee1f12447d49841dc9229cddcc9b10bf54f37566fdd74ecf11d")
        # Check store_date
        self.assertIsNotNone(file_store_date.find_item(value))

    @freeze_time("2022-03-08")
    def test_get_vaccine_date_no_ok_parameter(self):
        """tests no ok, date tests included here using test_ok.json file"""
        my_manager = VaccineManager()
        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        # Add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")

        # Added the date parameter for testing purposes
        for file_name, date, expected_value in param_list_nok:
            with self.subTest(test=file_name):
                file_test = JSON_FILES_RF2_PATH + file_name
                hash_original = file_store_date.data_hash()

                # Check the method
                with self.assertRaises(VaccineManagementException) as c_m:
                    my_manager.get_vaccine_date(file_test, date)
                self.assertEqual(c_m.exception.message, expected_value)

                # Read the file again to compare
                hash_new = file_store_date.data_hash()

                self.assertEqual(hash_new, hash_original)

    @freeze_time("2022-03-08")
    def test_get_vaccine_date_no_ok(self):
        """# long 32 in patient system id , not valid"""
        file_test = JSON_FILES_RF2_PATH + "test_no_ok.json"
        my_manager = VaccineManager()
        file_store_date = AppointmentsJsonStore()

        # Fixed Date in ISO format for testing purposes
        date = "2022-03-18"

        # read the file to compare file content before and after method call
        hash_original = file_store_date.data_hash()

        # Check the method
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.get_vaccine_date(file_test, date)
        self.assertEqual(c_m.exception.message, PatientSystemId.PATIENT_ID_NOT_VALID)

        # Read the file again to compare
        hash_new = file_store_date.data_hash()

        self.assertEqual(hash_new, hash_original)

    @freeze_time("2022-03-08")
    def test_get_vaccine_date_no_ok_no_quotes(self):
        """No quotes , not valid"""
        file_test = JSON_FILES_RF2_PATH + "test_nok_no_comillas.json"
        my_manager = VaccineManager()
        file_store_date = AppointmentsJsonStore()

        # Fixed Date in ISO format for testing purposes
        date = "2022-03-18"

        # Read the file to compare file content before and after method call
        hash_original = file_store_date.data_hash()

        # Check the method
        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.get_vaccine_date(file_test, date)
        self.assertEqual(c_m.exception.message, "JSON Decode Error - Wrong JSON Format")

        # Read the file again to compare
        hash_new = file_store_date.data_hash()

        self.assertEqual(hash_new, hash_original)

    @freeze_time("2022-03-08")
    def test_get_vaccine_date_no_ok_data_manipulated(self):
        """No quotes , not valid"""
        file_test = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()
        file_store = JSON_FILES_PATH + "store_patient.json"
        file_store_date = JSON_FILES_PATH + "store_date.json"

        if os.path.isfile(JSON_FILES_PATH + "swap.json"):
            os.remove(JSON_FILES_PATH + "swap.json")
        if not os.path.isfile(JSON_FILES_PATH + "store_patient_manipulated.json"):
            shutil.copy(JSON_FILES_RF2_PATH + "store_patient_manipulated.json",
                        JSON_FILES_PATH + "store_patient_manipulated.json")

        # Fixed Date in ISO format for testing purposes
        date = "2022-03-18"

        # Rename the manipulated patient's store
        if os.path.isfile(file_store):
            print(file_store)
            print(JSON_FILES_PATH + "swap.json")
            os.rename(file_store, JSON_FILES_PATH + "swap.json")
        os.rename(JSON_FILES_PATH + "store_patient_manipulated.json", file_store)

        file_store_date = AppointmentsJsonStore()
        # Read the file to compare file content before and after method call
        hash_original = file_store_date.data_hash()

        # Check the method

        exception_message = "Exception not raised"
        try:
            my_manager.get_vaccine_date(file_test, date)
        # pylint: disable=broad-except
        except Exception as exception_raised:
            exception_message = exception_raised.__str__()

        # Restore the original patient's store
        os.rename(file_store, JSON_FILES_PATH + "store_patient_manipulated.json")
        if os.path.isfile(JSON_FILES_PATH + "swap.json"):
            print(JSON_FILES_PATH + "swap.json")
            print(file_store)
            os.rename(JSON_FILES_PATH + "swap.json", file_store)

        # Read the file again to compare
        hash_new = file_store_date.data_hash()

        self.assertEqual(exception_message, "Patient's data have been manipulated")
        self.assertEqual(hash_new, hash_original)
