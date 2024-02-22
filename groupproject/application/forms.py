from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    avatar_choices=[('plant', 'Avatar 1'), ('water', 'Avatar 2'), ('fire', 'Avatar 3')]
    avatar_choice = forms.ChoiceField(
        choices = avatar_choices,
        widget=forms.Select(attrs={'onchange': 'updateAvatarPreview()'}),
        initial=avatar_choices[0][0],
        required=True
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "avatar_choice"]

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        # This will remove the 'helper' texts that django has by default (password is retained)
        for fieldname in ['username', 'email', 'password2', 'avatar_choice']:
            self.fields[fieldname].help_text = None 