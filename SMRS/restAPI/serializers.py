from rest_framework import serializers

## Remeber to import every model you use 
from restAPI.models import Project, Review, Defect, PhaseType, Product
from account.models import Team , Account


"""
*** This file is used to change your models into a json format that you can view.
    Model has to equal which model you are requiring to serialize.
    Fields allows to show what information from the database you want users to see.
    Offical : https://www.django-rest-framework.org/tutorial/1-serialization/
"""

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Team
        fields = ('id','name',)

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Project
        fields = ('id','name','productOwner','teamID','projectNumber')


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Review
        fields = ('id','dateOpened','dateClosed','projectID','whereFound','tag','severity','url')

class DefectSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Defect
        fields = ('id','dateOpened','dateClosed','description','projectID','whereFound','tag','severity','url')

class PhaseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PhaseType
        fields = ('id','phase_type')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Product
        fields = ('id','number', 'projectID')
        
class UserSerializer(serializers.ModelSerializer):
   class Meta:
        model = Account
        fields = ('name',)

