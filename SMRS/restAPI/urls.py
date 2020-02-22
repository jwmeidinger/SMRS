
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

from restAPI.views import (
    TeamView,
    ProjectView,
    DefectView,
    ReviewView,
    ProjectNumberView,
    PhaseTypeView,
    UserView
)
##import required views from the Rest API


##https://www.django-rest-framework.org/api-guide/routers/ for full documentation on routing
##There are two mandatory arguments to the register() method: Prefix - The URL prefix to use for this set of routes and viewset - The viewset class.




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
