from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import Profile
from django import forms


class CustomUserCreationForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=True, help_text='Enter your full name')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')
    class Meta:
        model = Profile
        fields = ('email',"name")


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = Profile
        fields = ('email',)

class SignUpForm(UserCreationForm):
    name = forms.CharField(max_length=30, required=True, help_text='Enter your full name')
    email = forms.EmailField(max_length=254, help_text='Enter a valid email address')

    class Meta:
        model = Profile
        fields = [
            'name',
            'email', 
            ]