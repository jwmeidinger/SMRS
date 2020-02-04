from django.shortcuts import render
from rest_framework import viewsets

from restAPI.models import Team, Project, Engineer, Review, Defect, ProjectNumber, PhaseType
from restAPI.serializers import(
TeamSerializer, ProjectSerializer, 
EngineerSerializer, ReviewSerializer,
DefectSerializer, ProjectNumberSerializer,
PhaseTypeSerializer,)


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

class ProjectNumberView(viewsets.ModelViewSet):
    queryset            = ProjectNumber.objects.all()
    serializer_class    = ProjectNumberSerializer

class PhaseTypeView(viewsets.ModelViewSet):
    queryset            = PhaseType.objects.all()
    serializer_class    = PhaseTypeSerializer