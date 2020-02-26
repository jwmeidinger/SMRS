from django.shortcuts import render
from django.shortcuts import render
from rest_framework import viewsets, permissions

from restAPI.models import Project, Review, Defect, ProjectNumber, PhaseType
from account.models import Team, Account






'''
*** Splash page
'''

def home_view(request):
    context= {}
    user = request.user
    if user.is_authenticated:
        context['message'] = 'Welcome to the Dashboard'
    return render(request, "dashboard/home.html", context)

def project_view(request):
    context= {}
    user = request.user
    if user.is_authenticated:
        project = Project.objects.all()
    return render(request, "dashboard/projects.html", context)

def team_view(request):
    context= {}
    user = request.user
    if user.is_authenticated:
        team = Team.objects.filter(pk = user.pk)
    return render(request, "dashboard/team.html", context)

