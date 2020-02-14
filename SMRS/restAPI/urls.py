
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

app_name = 'restAPI'

router = routers.DefaultRouter()
router.register('Team', TeamView)
router.register('Project', ProjectView)
router.register('Review', ReviewView)
router.register('Defect', DefectView)
router.register('ProjectNumber', ProjectNumberView)
router.register('PhaseType', PhaseTypeView)
router.register('Users',UserView)

urlpatterns = [
    path('', include(router.urls)),
    path('auth-token/', views.obtain_auth_token)
]
