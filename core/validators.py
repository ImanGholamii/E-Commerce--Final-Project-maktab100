from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, ValidationError
from django.utils.translation import gettext_lazy as _


class Validator:
    @staticmethod
    def phone_validator():
        return RegexValidator(regex=r'^(\+98|0)?9\d{9}$',
                              message=_("Phone number must be start with +98 or 0 in IR format."),
                              code=_('invalid IR phone number')
                              )

    @staticmethod
    def password_validator():
        def validate_password(value):
            if len(value) < 8 or not any(char.isalpha() for char in value) or not any(char.isdigit() for char in value):
                raise ValidationError(
                    _("Your password must contain at least 8 characters and include both letters and numbers."),
                    code='invalid_password'
                )

        return validate_password

    @staticmethod
    def email_validator():
        def validate_email(value):
            if get_user_model().objects.filter(email__iexact=value).exists():
                raise ValidationError(
                    _("This email is already in use. Please use a different email address."),
                    code='duplicate_email'
                )

        return validate_email
