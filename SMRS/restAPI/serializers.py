from rest_framework import serializers
from restAPI.models import Team, Project, Engineer, Review, Defect, Tool, Activity


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Team
        fields = ('id','team_title','team_projectid')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Project
        fields = ('id','project_title')

class EngineerSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Engineer
        fields = ('id','engineer_firstname','engineer_teamid')

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Review
        fields = ('id','review_title','review_defectid','review_projectid','review_toolid')

class DefectSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Defect
        fields = ('id','defect_title','defect_employeeid','defect_projectid','defect_toolid')

class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Tool
        fields = ('id','tool_name')

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model  = Activity
        fields = ('id','activity_type')