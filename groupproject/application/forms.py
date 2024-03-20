"""
Defines forms which will be used in the application

Author: Ashley Card, Maryia Fralova
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    avatar_choices=[('robin', 'Avatar 1'), ('seagull', 'Avatar 2'), ('wren', 'Avatar 3')]
    avatar_choice = forms.ChoiceField(
        choices = avatar_choices,
        widget=forms.Select(attrs={'onchange': 'updateAvatarPreview()'}),
        initial='Avatar 1'
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", "avatar_choice")

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        # This will remove the 'helper' texts that django has by default (password is retained)
        for fieldname in ['username', 'email', 'password2', 'avatar_choice']:
            self.fields[fieldname].help_text = None 

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model  = Profile
        fields = ['avatar_choice']