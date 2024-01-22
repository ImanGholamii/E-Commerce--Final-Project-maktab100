from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, ReadOnlyPasswordHashField
from django import forms
from django.utils.translation import gettext_lazy as _


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = [_('username'), _('email'), _('phone'), _('password1'), _('password2'), _('is_customer')
                  ]
        labels = {
            'is_customer': 'Customer'
        }



class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="<a href=\"../password/\">Change password</a>")

    class Meta:
        model = get_user_model()
        fields = "__all__"
