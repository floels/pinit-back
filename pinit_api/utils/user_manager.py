from django.contrib.auth.models import BaseUserManager


# https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#a-full-example
class UserManager(BaseUserManager):
    def create_user(self, email, birthdate=None, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            birthdate=birthdate,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, birthdate=None, password=None):
        user = self.create_user(
            email,
            password=password,
            birthdate=birthdate,
        )
        user.is_admin = True
        user.save(using=self._db)

        return user
