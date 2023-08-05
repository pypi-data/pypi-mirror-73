from unittest import TestCase

from main.validation_handling import validate_longitude_latitude, validate_google_sample_number


class TestValidationHandling(TestCase):
    def test_validate_longitude_latitude_type(self):
        self.assertRaises(TypeError, validate_longitude_latitude, "Hello", 44.444)

    def test_validate_longitude_latitude_value(self):
        self.assertRaises(ValueError, validate_longitude_latitude, 999.999, 55.555)

    def test_validate_google_sample_number_value(self):
        self.assertRaises(ValueError, validate_google_sample_number, -1)

    def test_validate_google_sample_number_type(self):
        self.assertRaises(TypeError, validate_google_sample_number, "32233")
