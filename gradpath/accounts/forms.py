from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser 
        fields = ['username', 'email', 'phone_number', 'graduation_year', 'password1', 'password2']
