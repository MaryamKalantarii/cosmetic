from django.contrib.auth import forms as auth_forms
from django.core.exceptions import ValidationError
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomeUser, Profile



class AuthenticationForm(auth_forms.AuthenticationForm):
    def confirm_login_allowed(self, user):
        super(AuthenticationForm,self).confirm_login_allowed(user)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomeUser
        fields = ['email', 'password1', 'password2']  # فقط فیلدهای CustomeUser

