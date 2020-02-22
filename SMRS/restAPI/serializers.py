from rest_framework import serializers
from restAPI.models import Project, Review, Defect, PhaseType, ProjectNumber
from account.models import Team , Account
##Remeber to import every model you use 


##Use your model snippet and Serializer with serializer.ModelSerializer as paramater to create a Model serializer
##Model has to equal which model you are requiring to serialize
##Fields allows to show what information from the database you want users to see
##https://www.django-rest-framework.org/tutorial/1-serialization/ for the full documentation
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Team
        fields = ('id','name',)

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Project
        fields = ('id','name','productOwner','teamID')


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
        
class UserSerializer(serializers.ModelSerializer):
   class Meta:
        model = Account
        fields = ('name',)


### this will be used if they would like to view the foreign key as the name instead of the primary key
"""
def to_representation(self, instance):
    ###Convert `username` to lowercase.
    ret = super().to_representation(instance)
    ret['username'] = ret['username'].lower()
    return ret
"""