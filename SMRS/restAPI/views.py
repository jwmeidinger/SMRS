from django.shortcuts import render
from rest_framework import viewsets, permissions

from restAPI.models import Project, Review, Defect, Product, PhaseType
from account.models import Team, Account

from restAPI.serializers import(
TeamSerializer, ProjectSerializer,
ReviewSerializer,DefectSerializer,
ProductSerializer, PhaseTypeSerializer,
UserSerializer)

"""
*** This file is bringing everything together and handles all of viewing and requests.
    Need to provide at least the queryset and serializer_class attributes.
    Permission class allows for read only or IsAuthenticatedOrReadOnly allowing for only users that have permission to edit.
    Offical : https://www.django-rest-framework.org/api-guide/viewsets/
    Offical : https://docs.djangoproject.com/en/3.0/topics/http/views/
"""

class TeamView(viewsets.ModelViewSet):
    queryset            = Team.objects.all()
    serializer_class    = TeamSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class ProjectView(viewsets.ModelViewSet):
    queryset            = Project.objects.all()
    serializer_class    = ProjectSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class ReviewView(viewsets.ModelViewSet):
    queryset            = Review.objects.all()
    serializer_class    = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class DefectView(viewsets.ModelViewSet):
    queryset            = Defect.objects.all()
    serializer_class    = DefectSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class ProductView(viewsets.ModelViewSet):
    queryset            = Product.objects.all()
    serializer_class    = ProductSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class PhaseTypeView(viewsets.ModelViewSet):
    queryset            = PhaseType.objects.all()
    serializer_class    = PhaseTypeSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

class UserView(viewsets.ModelViewSet):
    queryset            = Account.objects.all()
    serializer_class    = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)