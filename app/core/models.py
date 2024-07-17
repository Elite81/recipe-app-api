''' Database Models '''
from django.db import models  # noqa
from django.contrib.auth.models import(
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)

# Create your models here.

class UserManager(BaseUserManager):
    '''Manager for users'''

    def create_user(self, email, password=None, **extra_fields):
        ''' Create, save and return  anew user.'''
        if not email:
            raise ValueError('usermust have email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        '''Create and reaturn a new superuser.'''
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    '''User in the System '''
    email  = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active= models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    object = UserManager()

    USERNAME_FIELD = 'email'