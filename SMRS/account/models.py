
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser

## Team needs to be in Account app as it is required by the AbstractBaseUser

class Team (models.Model):
    name                     = models.CharField(max_length=25) ## change to uniq

    def __str__(self):
        return self.name


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

class Account(AbstractBaseUser):

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name                = models.TextField()
    racf                = models.CharField(max_length=30, unique=True)
    teamid              = models.ForeignKey(Team, blank = True, null = True, on_delete=models.CASCADE)
    ## Items required
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


