from django.contrib import admin

from restAPI.models import Project, Review, Defect, ProjectNumber, PhaseType
# Register your models here.

admin.site.register(Project)
admin.site.register(Review)
admin.site.register(Defect)
admin.site.register(ProjectNumber)
admin.site.register(PhaseType)