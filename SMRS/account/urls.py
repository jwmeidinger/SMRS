from django.urls import path
from .views import (
    registration_view,
    logout_view,
    login_view,
    must_authenticate,)

app_name = 'account'
urlpatterns = [
    path('register/', registration_view,name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login'),
    path('must_authenticate/', must_authenticate, name='must_authenticate'),
]