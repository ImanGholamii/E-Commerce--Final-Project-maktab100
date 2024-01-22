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