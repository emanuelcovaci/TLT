from django.core.validators import validate_email
from django import forms

from captcha.fields import ReCaptchaField
from .models import ContactUs


class CreateContact(forms.ModelForm):

    captcha = ReCaptchaField()

    class Meta:
        model = ContactUs
        fields = '__all__'
        widgets = {
            'email': forms.EmailInput({'required': 'required',
                                       'placeholder': 'Email'}),
            'message': forms.Textarea(attrs={'required': 'required',
                                             'placeholder': 'Message'})
        }

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise forms.ValidationError("Introdu un prenume valid")
        return first_name

    def clean_email(self):
        email = self.cleaned_data['email']
        if validate_email(email):
            raise forms.ValidationError("Adresa de email nu e valida")
        return email

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalpha():
            raise forms.ValidationError("Introdu un nume corect")
        return last_name

    def clean_message(self):
        message = self.cleaned_data['message']
        if len(message) < 50:
            raise forms.ValidationError(
                "Mesajul tau e prea scurt!"
                "Trebuie sa contina minim 50 de caractere")
        return message