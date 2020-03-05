from django.urls import path

from .views import(
    team_view,
    project_view,
    projectDetail_view,
    defect_view,
    review_view,
    projectAddFav_view,
    projectDelFav_view,

)




"""
*** This file is used to keep track of all the urls for this App
    If you would like to look at all the urls go to the SMRS app urls.py
    Offical : https://docs.djangoproject.com/en/3.0/topics/http/urls/
"""

app_name = 'dashboard'
urlpatterns = [
    
    path('projects/', project_view, name='project'),
    path('team/', team_view, name='team'),
    path('project/<int:pk>', projectDetail_view, name='detail'),
    path('review/<int:pk>', review_view, name='reviewDetail'),
    path('defect/<int:pk>', defect_view, name='defectDetail'),
    path('addfav/<int:pk>', projectAddFav_view, name='addfav'),
    path('delfav/<int:pk>', projectDelFav_view, name='delfav'),
    
]