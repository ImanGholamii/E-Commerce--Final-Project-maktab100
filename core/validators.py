from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _


class Validator:
    @staticmethod
    def phone_validator():
        return RegexValidator(regex=r'^(\+98|0)?9\d{9}$',
                              message=_("Phone number must be start with +98 or 0 in IR format."),
                              code=_('invalid IR phone number')
                              )
