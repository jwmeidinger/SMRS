
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

## Import views from the Rest API
from restAPI.views import (
    TeamView,
    ProjectView,
    DefectView,
    ReviewView,
    ProjectNumberView,
    PhaseTypeView,
    UserView
)
"""
*** This file is used to route all of the API urls.
    There are two mandatory arguments to the register() method:
    The URL prefix to use for this set of routes and viewset
    The viewset class
    Offical : https://www.django-rest-framework.org/api-guide/routers/
"""

app_name = 'restAPI'

router = routers.DefaultRouter()
router.register('Team', TeamView)
router.register('Project', ProjectView)
router.register('Review', ReviewView)
router.register('Defect', DefectView)
router.register('ProjectNumber', ProjectNumberView)
router.register('PhaseType', PhaseTypeView)
router.register('Users',UserView)

## The .urls attribute on a router instance is simply a standard list of URL patterns
## If using namespacing with hyperlinked serializers you'll also need to ensure that any view_name parameters on the serializers correctly reflect the namespace.

urlpatterns = [
    path('', include(router.urls)),
    path('auth-token/', views.obtain_auth_token)
]
