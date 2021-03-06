
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

"""
*** This file is used to create the Database.
    It uses Django ORM which allows for easy queries later on.
    Each model is a Python class that subclasses django.db.models.Model.
    Each field is specified as a class attribute, and each attribute maps to a database column.
    With all of this, Django gives you an automatically-generated database-access API
    Offical : https://docs.djangoproject.com/en/3.0/topics/db/models/
    Offical : https://docs.djangoproject.com/en/3.0/ref/models/fields/#common-model-field-options
"""

Theme = [
    ('Light', 'Light'),
    ('Dark', 'Dark'),
]

"""
*** Team needs to be in Account app as it is required by the AbstractBaseUser
"""
class Team (models.Model):
    name                     = models.CharField(max_length=25, unique=True )
    teamData                 = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.name

"""
*** This Account manager is used to create a new user.
    The reason this is created as it allows to create different premissions
"""
class MyAccountManager(BaseUserManager):
    def create_user(self, email, name, racf, password=None):
        # Creates and saves a User with the given email and password.
        if not email:
            raise ValueError('User must have an email address')
        if not name:
            raise ValueError('User must have an Name')
        if not racf:
            raise ValueError('User must have an Racf')
        
        user = self.model(
            email = self.normalize_email(email),
            name = name,
            racf = racf,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, name, racf, password):
        # Creates and saves a staff user with the given email and password
        user = self.create_user(
            email = self.normalize_email(email),
            name = name,
            racf = racf,
            password = password,
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, racf, password):
        # Creates and saves a admin user with the given email and password
        user = self.create_user(
            email = self.normalize_email(email),
            name = name,
            racf = racf,
            password = password,
        )
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

"""
*** This Account is the custom user for Django
    The reason this is created as it allows to create new field such as
    email, racf, teamid, ect.
"""
class Account(AbstractBaseUser):

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name                = models.TextField()
    racf                = models.CharField(max_length=30, unique=True)
    darkColorScheme     = models.CharField(choices=Theme, default="Light", max_length=10)
    teamid              = models.ForeignKey(Team, blank = True, null = True, on_delete=models.CASCADE)
    ## Items required by AbstratctBaseUser
    date_joined         = models.DateTimeField(auto_now_add=True, editable=False)
    last_login          = models.DateTimeField(auto_now=True)
    is_active           = models.BooleanField(default=True)
    is_staff            = models.BooleanField(default=False) # admin user, non super-user
    is_admin            = models.BooleanField(default=False) # admin 
    is_superuser        = models.BooleanField(default=False) # superuser
    # Password is build in with the AbstratctBaseUser

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','racf'] # username (email) and password are required by default.

    # Uses the Class above to create new Users
    objects = MyAccountManager()

    # If we want to get the users name
    def get_full_name(self):
        return self.name
    
    # The user email
    def get_email(self):
        return self.email

    def __str__(self):
        return self.email

    # Check if user is Admin
    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

"""
*** Generate new Auth token for every new user.
    You can remove tokens in the admin Portal
"""
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)

