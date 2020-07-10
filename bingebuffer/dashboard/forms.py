from django import forms
from . import models
from django.forms.widgets import DateInput
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.Userprofile
        fields = ['nickname', 'date_of_birth', 'badge']
        widgets = {
        'date_of_birth': DateInput(attrs={'type': 'date'})
        }

class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = {
            'first_name', 'last_name', 'email', 'password'
        }