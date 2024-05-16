from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"autofocus": True,
                                                             # 'class': 'form-group',
                                                             'placeholder': 'Введите логин'}))
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password",
                                          # 'class': 'form-group',
                                          'placeholder': 'Введите пароль'}),)
    class Meta:
        model = User
        fields = ['username', 'password']
