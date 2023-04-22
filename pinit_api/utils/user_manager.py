from django.contrib.auth.models import BaseUserManager


# https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#a-full-example
class UserManager(BaseUserManager):
    def create_user(
        self,
        email,
        password=None,
        birthdate=None,
        username=None,
        initial=None,
        first_name=None,
        last_name=None,
    ):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            birthdate=birthdate,
            username=username,
            initial=initial,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)

        return user
