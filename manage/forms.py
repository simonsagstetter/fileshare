from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import EmailInput
from django.utils.translation import gettext, gettext_lazy as _

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Email Address"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': _('Email Address')}),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Password')}),
    )
