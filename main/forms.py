from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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
    email = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Hasło'}))


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


class UserProfile(forms.Form):
    username = forms.CharField(max_length=100, label="Username")
    first_name = forms.CharField(max_length=30, label="Imię")
    last_name = forms.CharField(max_length=30, label="Nazwisko")
    email = forms.EmailField(max_length=254, label="E-mail")