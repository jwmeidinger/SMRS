from django.shortcuts import render
from rest_framework import viewsets

from restAPI.models import Team, Project, Engineer, Review, Defect, Tool, Activity
from restAPI.serializers import(
TeamSerializer, ProjectSerializer, 
EngineerSerializer, ReviewSerializer,
DefectSerializer, ToolSerializer,
ActivitySerializer)


class TeamView(viewsets.ModelViewSet):
    queryset            = Team.objects.all()
    serializer_class    = TeamSerializer

class ProjectView(viewsets.ModelViewSet):
    queryset            = Project.objects.all()
    serializer_class    = ProjectSerializer

class EngineerView(viewsets.ModelViewSet):
    queryset            = Engineer.objects.all()
    serializer_class    = EngineerSerializer

class ReviewView(viewsets.ModelViewSet):
    queryset            = Review.objects.all()
    serializer_class    = ReviewSerializer

class DefectView(viewsets.ModelViewSet):
    queryset            = Defect.objects.all()
    serializer_class    = DefectSerializer

class ToolView(viewsets.ModelViewSet):
    queryset            = Tool.objects.all()
    serializer_class    = ToolSerializer

class ActivityView(viewsets.ModelViewSet):
    queryset            = Activity.objects.all()
    serializer_class    = ActivitySerializer