## Author: Jordan Meidinger
## Date: Fall 2019

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account, Team

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')
    teamid = forms.ModelChoiceField(queryset=Team.objects.all())

    class Meta:
        model = Account
        fields = ('email', 'name', 'racf', 'teamid','password1', 'password2')

class AccountAuthenticationForm(forms.ModelForm):
    
    password = forms.CharField( widget=forms.PasswordInput)

    class Meta:
        model = Account
        fields = ('email','password')

    def clean(self):
        if self.is_valid:
            email = self.cleaned_data['email']
            password= self.cleaned_data['password']
            if not authenticate(email= email, password= password):
                raise forms.ValidationError("Incorrect email or password")
        


