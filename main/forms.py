from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Donation


class UserRegister(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label="Imię")
    last_name = forms.CharField(max_length=30, required=True, label="Nazwisko")
    email = forms.EmailField(max_length=254, required=True, label="E-mail")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            field = self.fields.get(field_name)
            self.fields[field_name].widget.attrs.update({
                "placeholder": field.label,
            })


class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))


class DonationForm(forms.ModelForm):
    class Meta:
        model = Donation
        fields = [
            'categories',
            'quantity',
            'institution',
            'address',
            'phone_number',
            'city',
            'zip_code',
            'pick_up_date',
            'pick_up_time',
            'pick_comment'
        ]


class UserSettings(forms.Form):
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.EmailField(max_length=254, widget=forms.EmailInput(attrs={'placeholder': 'E-mail'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    password_repeat = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))

    def clean(self):
        cleaned_data = super().clean()
        print(cleaned_data)
        if cleaned_data['password'] != cleaned_data['password_repeat']:
            self.add_error('password', 'Hasła nie są identyczne')
            self.add_error('password_repeat', 'Hasła nie są identyczne')
            raise forms.ValidationError("Podano różne hasła")
        return cleaned_data
