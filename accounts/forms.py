from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Subscription


class RegisterForm(UserCreationForm):
    # extends Django's built in UserCreationForm
    # already has username, password1, password2 fields

    email = forms.EmailField(
        required=True,
        help_text='Required. Enter a valid email address.'
    )

    plan = forms.ChoiceField(
        choices=Subscription.PLAN_CHOICES,
        help_text='Select your subscription plan'
        # shows plan options during registration
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'plan']
        # fields shown in the registration form