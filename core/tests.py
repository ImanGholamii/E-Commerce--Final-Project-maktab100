from django.test import TestCase
from django.core.exceptions import ValidationError
from core.validators import Validator
from django.utils.translation import gettext_lazy as _


class ValidatorTest(TestCase):
    def test_phone_validator_invalid_prefix(self):
        phone_validator = Validator.phone_validator()
        invalid_phone_number = '989123456789'  # Missing +

        with self.assertRaises(ValidationError) as context:
            phone_validator(invalid_phone_number)

        expected_error_message = _("Phone number must be start with +98 or 0 in IR format.")
        self.assertEqual(context.exception.messages, [expected_error_message])

    def test_phone_validator_invalid_format(self):
        phone_validator = Validator.phone_validator()
        invalid_phone_number = '+14155552671'  # US phone number

        with self.assertRaises(ValidationError) as context:
            phone_validator(invalid_phone_number)

        expected_error_message = _("Phone number must be start with +98 or 0 in IR format.")
        self.assertEqual(context.exception.messages, [expected_error_message])

    def test_phone_validator_invalid_number(self):
        phone_validator = Validator.phone_validator()
        invalid_phone_number = '123456789'

        with self.assertRaises(ValidationError) as context:
            phone_validator(invalid_phone_number)

        expected_error_message = _("Phone number must be start with +98 or 0 in IR format.")
        self.assertEqual(context.exception.messages, [expected_error_message])

    def test_phone_validator_valid_number(self):
        phone_validator = Validator.phone_validator()
        valid_phone_number = '+989123456789'

        try:
            phone_validator(valid_phone_number)
        except ValidationError:
            self.fail("Validation Error raised for a valid phone number.")
