
from django.urls import path, include
from rest_framework import routers

from restAPI.views import (
    TeamView,
    ProjectView,
    ToolView,
    DefectView,
    EngineerView,
    ReviewView,
    ActivityView,)

app_name = 'restAPI'

router = routers.DefaultRouter()
router.register('Team', TeamView)
router.register('Project', ProjectView)
router.register('Engineer', EngineerView)
router.register('Review', ReviewView)
router.register('Defect', DefectView)
router.register('Activity', ActivityView)
router.register('Tool', ToolView)

urlpatterns = [
    path('', include(router.urls)),
]
