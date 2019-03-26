from django import forms
from django.contrib.auth.forms import UserCreationForm

from users.models import User


class UserSignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        user_exists = User.objects.filter(email=email).exists()
        if user_exists:
            raise forms.ValidationError('A user account with this email already exists!')
        return email
