
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account, Team

"""
*** This file is used to create Forms
    It allows for easy validation and database input
    Offical : https://docs.djangoproject.com/en/3.0/topics/db/models/
"""

"""
*** Used to create new users 
    not implmemented right now as it's not required on homepage.
"""
class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text='Required. Add a valid email address')
    teamid = forms.ModelChoiceField(queryset=Team.objects.all())

    class Meta:
        model = Account
        fields = ('email', 'name', 'racf', 'teamid','password1', 'password2')

"""
*** Used to Login 
"""
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
        
class AccountUpdateForm(forms.ModelForm):

    last_name = forms.CharField( max_length= 15, required=False) ## This needs to be here to make it not required in the form

    class Meta:
        model = Account
        fields = ('email', 'name', 'racf', 'teamid', 'darkColorScheme')
        

    def clean_email(self):
        if self.is_valid:
            email = self.cleaned_data['email']
            try:
                account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
            except:
                return email
            raise forms.ValidationError('Email "%s" is already in use.' % email)
            
            




