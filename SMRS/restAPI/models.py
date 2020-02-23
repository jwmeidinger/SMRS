from django.db import models

import account.models as model


"""
*** This file is used to create the Database.
    It uses Django ORM which allows for easy queries later on.
    Each model is a Python class that subclasses django.db.models.Model.
    Each field is specified as a class attribute, and each attribute maps to a database column.
    With all of this, Django gives you an automatically-generated database-access API
    Offical : https://docs.djangoproject.com/en/3.0/topics/db/models/
    Offical : https://docs.djangoproject.com/en/3.0/ref/models/fields/#common-model-field-options
"""

MajorMinorChoices = [
    ('Minor', 'Minor'),
    ('Major', 'Major'),
]

## Django creates the ID Automaticly  

class PhaseType (models.Model):
    phase_type               = models.CharField(max_length=25) # type can't be used need to be renamed
    
    def __str__(self):
        return self.phase_type


class Project (models.Model):
    name                    = models.CharField(max_length=25)
    productOwner            = models.ForeignKey(model.Account, null = True, blank = True, on_delete=models.CASCADE)
    teamID                  = models.ForeignKey(model.Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Defect (models.Model):
    dateOpened              = models.DateField(auto_now=False, auto_now_add=False)
    dateClosed              = models.DateField(blank=True, null=True)
    projectID               = models.ForeignKey(Project, on_delete=models.CASCADE)
    whereFound              = models.ForeignKey(PhaseType, on_delete=models.CASCADE)
    tag                     = models.CharField(max_length=50) ## change to uniq
    severity                = models.CharField(choices=MajorMinorChoices,max_length=25)
    url                     = models.URLField(max_length=200) ## change to uniq

    def __str__(self):
        return self.tag


class Review (models.Model):
    dateOpened              = models.DateField(auto_now=False, auto_now_add=False)
    dateClosed              = models.DateField(blank=True, null=True)
    projectID               = models.ForeignKey(Project, on_delete=models.CASCADE)
    whereFound              = models.ForeignKey(PhaseType, on_delete=models.CASCADE)
    tag                     = models.CharField(max_length=50) ## change to uniq
    severity                = models.CharField(choices=MajorMinorChoices,max_length=25)
    url                     = models.URLField(max_length=200) ## change to uniq

    def __str__(self):
        return self.tag


class ProjectNumber (models.Model):
    number              = models.IntegerField()
    projectID           = models.ForeignKey(Project, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.number)