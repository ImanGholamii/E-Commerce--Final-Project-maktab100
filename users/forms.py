from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=(('customer', _('Customer')), ('employee', _('Employee'))))

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email', 'phone', 'gender', 'date_of_birth',
                  'user_type', 'password1', 'password2'
                  ]
