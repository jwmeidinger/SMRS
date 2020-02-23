from django.contrib import admin

from restAPI.models import Project, Review, Defect, ProjectNumber, PhaseType

"""
*** This is file is used to add items to the admin portal
    Can be very powerful to so advanced searches and customizability 
    Offical : https://docs.djangoproject.com/en/3.0/ref/contrib/admin/
"""

admin.site.register(Project)
admin.site.register(Review)
admin.site.register(Defect)
admin.site.register(ProjectNumber)
admin.site.register(PhaseType)