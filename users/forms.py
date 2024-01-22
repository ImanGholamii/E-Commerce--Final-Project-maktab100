from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from django import forms
from django.utils.translation import gettext_lazy as _
from core.validators import Validator


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email', 'phone', 'password1', 'password2', 'is_customer']
        labels = {
            'is_customer': _('Customer')
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        password_validator = Validator.password_validator()
        self.fields['password1'].validators.append(password_validator)

        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

        email_validator = Validator.email_validator()
        self.fields['email'].validators.append(email_validator)

        self.fields['email'].error_messages = {
            'duplicate_email': _('This email is already in use. Please use a different email address.'),
        }

        phone_validator = Validator.phone_validator()
        self.fields['phone'].validators.append(phone_validator)

        self.fields['phone'].help_text = ''

        self.fields['phone'].error_messages = {
            'invalid': _('Invalid phone number. Please must be start with +98 or 0'),
            'duplicate_phone': _('This phone number is already in use. Please use a different phone number.'),
        }

    def add_error(self, field, error):
        super().add_error(field, error)
        if field in self.errors:
            self.fields[field].widget.attrs.update({'class': 'error-message'})


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="<a href=\"../password/\">Change password</a>")

    class Meta:
        model = get_user_model()
        fields = "__all__"
