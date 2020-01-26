from django.contrib import admin

from restAPI.models import Team, Project, Engineer, Review, Defect, Tool, Activity
# Register your models here.

admin.site.register(Team)
admin.site.register(Project)
admin.site.register(Engineer)
admin.site.register(Review)
admin.site.register(Defect)
admin.site.register(Tool)
admin.site.register(Activity)