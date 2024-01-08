from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


class customUserCreationForm(UserCreationForm):
    # user_type = forms.ChoiceField(choices=(('customer', 'Customer'), ('employee', 'Employee')))
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email', 'phone', 'address', 'gender', 'date_of_birth',
                  'user_type', 'password1', 'password2'
                  ]