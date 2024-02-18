from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from django import forms
from django.utils.translation import gettext_lazy as _
from core.validators import Validator
from users.models import Employee, UserProfile, Address


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email', 'phone', 'password1', 'password2']
        # labels = {
        #     'is_customer': _('Customer')
        # }

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


class EmployeeCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=Employee.ROLE_CHOICES, label='Role')

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'phone', 'password1', 'password2', 'role']
        labels = {
            # 'is_employee': _('Employee'),
            'role': _('Role'),
        }

    def __init__(self, *args, **kwargs):
        super(EmployeeCreationForm, self).__init__(*args, **kwargs)

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

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_customer = False
        user.is_employee = True

        if commit:
            user.save()
        return user


class VerifyCodeForm(forms.Form):
    code = forms.IntegerField()


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="<a href=\"../password/\">Change password</a>")

    class Meta:
        model = get_user_model()
        fields = "__all__"


class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()

    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'gender', 'date_of_birth', 'bio', 'social_media', 'interests', 'addresses',
                  'first_name', 'last_name']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['state', 'city', 'street', 'alley', 'no', 'unit_number', 'postal_code', 'is_default',
                  'additional_info']
        widgets = {
            'user': forms.HiddenInput(),
        }
