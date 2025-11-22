from django import forms
from django.contrib.auth.forms import UserCreationForm
from user_auths.models import CustomUser

class CustomUserRegistrationForm(UserCreationForm):
    
    class Meta: 
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email address'}),
        }