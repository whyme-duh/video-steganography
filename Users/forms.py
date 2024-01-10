from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from . models import Profile

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required= False)

    class Meta:
        model = User
        fields = ['username',  ]


