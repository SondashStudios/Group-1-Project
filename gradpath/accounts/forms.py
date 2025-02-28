from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser  # Ensure this matches the model in models.py
        fields = ['username', 'email', 'phone_number', 'graduation_year', 'password1', 'password2']
