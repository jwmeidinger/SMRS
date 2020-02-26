from django.urls import path
from .views import (
    registration_view,
    logout_view,
    login_view,
    must_authenticate,)

"""
*** This file is used to keep track of all the urls for this App
    If you would like to look at all the urls go to the SMRS app urls.py
    Offical : https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""
app_name = 'account'
urlpatterns = [
    path('register/', registration_view,name='register'), #If you want people to register on the homepage
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('must_authenticate/', must_authenticate, name='must_authenticate'),
]