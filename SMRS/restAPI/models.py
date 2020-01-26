from django.db import models


## Django creates the ID Automaticly  

class Project (models.Model):
    project_title           = models.CharField(max_length=25)
    project_description     = models.CharField(max_length=200)
    
    def __str__(self):
        return self.project_title


class Tool (models.Model):
    tool_name               = models.CharField(max_length=25)
    
    def __str__(self):
        return self.tool_name

class Team (models.Model):
    team_title              = models.CharField(max_length=25)
    team_projectid          = models.ManyToManyField(Project)

    def __str__(self):
        return self.team_title


class Engineer (models.Model):
    engineer_firstname      = models.CharField(max_length=25) 
    engineer_teamid         = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.engineer_firstname


class Defect (models.Model):
    defect_title            = models.CharField(max_length=25)
    defect_employeeid       = models.ForeignKey(Engineer, on_delete=models.CASCADE)
    defect_projectid        = models.ForeignKey(Project, on_delete=models.CASCADE)
    defect_toolid           = models.ForeignKey(Tool, on_delete=models.CASCADE)

    def __str__(self):
        return self.defect_title

class Activity (models.Model):
    activity_type           = models.CharField(max_length=25, null=False, blank=False, unique=True) # switch this to selection later

    def __str__(self):
        return self.activity_type


class Review (models.Model):
    review_title            = models.CharField(max_length=25)
    review_defectid         = models.ManyToManyField(Defect)
    review_toolid           = models.ForeignKey(Tool, on_delete=models.CASCADE)
    review_projectid        = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.review_title