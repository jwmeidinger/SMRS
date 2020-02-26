
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from account.models import Team
from account.forms import RegistrationForm, AccountAuthenticationForm

'''
*** This file is used to grab information and put it into the html
    Main items for each function is Request, Context, and Template
    Offical : https://docs.djangoproject.com/en/3.0/topics/http/views/
'''




'''
*** Create new account
    Need to Un-commment in urls and templates/snippets/header.html 
    If you would like to create new users on the home page
'''
def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        context['registation_form'] = form
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registation_form'] = form
    else:
        form = RegistrationForm()
        context['registation_form'] = form
    return render (request, 'account/register.html', context)

'''
*** Log Out account
'''
def logout_view(request):
    logout(request)
    return redirect('home')

'''
*** Log In account
'''
def login_view(request):
    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("home")
    
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login (request, user)
                return redirect('home')
    else:
        form = AccountAuthenticationForm()

    context['form'] = form
    return render(request, 'account/login.html', context)

'''
*** Account not logged in
'''
def must_authenticate(request):
    return render(request,'account/must_authenticate.html', {})