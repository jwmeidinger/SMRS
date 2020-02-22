from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from account.models import Account, Team

"""
*** This is file is used to add items to the admin portal
    Can be very powerful to so advanced searches and customizability 
    Offical : https://docs.djangoproject.com/en/3.0/ref/contrib/admin/
"""

"""
*** Used to create users in the Admin
    if you didn't do this it would use the default account in django.
"""
class UserCreateForm(UserCreationForm):
    class Meta:
        model = Account
        fields = ('email',)

class AccountAdmin(UserAdmin):
    # Displays accounts better on the view
    list_display = ('email', 'date_joined', 'last_login', 'is_admin')
    # Used to search People at top of view
    search_fields = ('email','racf',)
    readonly_fields = ('date_joined', 'last_login')
    # Is required by the UserAdmin
    filter_horizontal = ()
    list_filter = ()

    # Needed to create new User with the correct format
    add_form = UserCreationForm
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name','racf','teamid')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),)
    ordering = ('email',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','name','racf','teamid','password1', 'password2'),}),)

## lastly resgister the items for this app
admin.site.register(Account, AccountAdmin)
admin.site.register(Team)