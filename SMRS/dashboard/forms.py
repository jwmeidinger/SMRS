from django import forms

from restAPI.models import Review, Defect, Project, PhaseType

"""
*** This file is used to create Forms
    It allows for easy validation and database input
    Offical : https://docs.djangoproject.com/en/3.0/topics/db/models/
"""


class DefectForm(forms.ModelForm):

    dateClosed = forms.DateField(required=False)

    class Meta:
        model = Defect
        fields = ('dateOpened','dateClosed','projectID','whereFound','tag','severity','url')




class ReviewForm(forms.ModelForm):

    dateClosed = forms.DateField(required=False)

    class Meta:
        model = Review
        fields = ('dateOpened','dateClosed','projectID','whereFound','tag','severity','url')
