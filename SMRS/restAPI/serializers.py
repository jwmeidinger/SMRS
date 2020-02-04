from rest_framework import serializers
from restAPI.models import Team, Project, Engineer, Review, Defect, PhaseType, ProjectNumber


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Team
        fields = ('id','name',)

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Project
        fields = ('id','name','productOwner','teamID')

class EngineerSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Engineer
        fields = ('id','name','racf','teamID')

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Review
        fields = ('id','dateOpened','dateClosed','projectID','whereFound','tag','severity','url')

class DefectSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Defect
        fields = ('id','dateOpened','dateClosed','projectID','whereFound','tag','severity','url')

class PhaseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PhaseType
        fields = ('id','phase_type')

class ProjectNumberSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ProjectNumber
        fields = ('id','number', 'projectID')