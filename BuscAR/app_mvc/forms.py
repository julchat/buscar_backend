from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from app_mvc.models import Account

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=255, help_text="Requerido.")

    class Meta:
        model = Account
        fields = ('email', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email'].lower()  # IT MUST MATCH WITH FILED IN REGISTER.HTML
        try:
            account = Account.objects.get(email=email)
        except Exception as e:
            return email
        raise forms.ValidationError(f"Email {email} ya está en uso.")

    def clean_username(self):
        username = self.cleaned_data['username'].lower()  # IT MUST MATCH WITH FILED IN REGISTER.HTML
        try:
            account = Account.objects.get(email=username)
        except Exception as e:
            return username
        raise forms.ValidationError(f"Usuario {username} ya está en uso.")

