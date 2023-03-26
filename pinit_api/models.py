from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .utils.user_manager import UserManager


class User(AbstractBaseUser):
    # See https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#specifying-a-custom-user-model
    email = models.EmailField(unique=True)
    birthdate = models.DateField(null=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
