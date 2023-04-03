from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class RegistrationUserForm(UserCreationForm):

    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'registration_form_item_inp'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'registration_form_item_inp'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'registration_form_item_inp'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'registration_form_item_inp'}))


    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class AuthorisationUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'authorisation_form_item_inp'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'authorisation_form_item_inp'}))