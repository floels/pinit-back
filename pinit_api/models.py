import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .utils.user_manager import UserManager


class User(AbstractBaseUser):
    # See https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#specifying-a-custom-user-model
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    birthdate = models.DateField(blank=True, null=True)
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


class Account(models.Model):
    username = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50)  # "personal" or "business"
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    business_name = models.CharField(max_length=100, blank=True, null=True)
    initial = models.CharField(max_length=1, blank=True, null=True)
    profile_picture_url = models.URLField(blank=True, null=True)
    background_picture_url = models.URLField(blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    saved_pins = models.ManyToManyField(
        "Pin", through="SavedPin", related_name="saved_by"
    )

    @property
    def display_name(self):
        if self.type == "personal":
            return f"{self.first_name} {self.last_name}"

        return self.business_name

    def __str__(self):
        return self.username


class Pin(models.Model):
    unique_id = models.CharField(max_length=18, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    author = models.ForeignKey(Account, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = self.generate_unique_id()
        super(Pin, self).save(*args, **kwargs)

    @staticmethod
    def generate_unique_id():
        while True:
            # Generate a random 18-digit number:
            tentative_unique_id = random.randint(
                100_000_000_000_000_000, 999_999_999_999_999_999
            )

            tentative_unique_id_string = str(tentative_unique_id)

            if not Pin.objects.filter(unique_id=tentative_unique_id_string).exists():
                return tentative_unique_id_string

    def __str__(self):
        return f"Pin {self.unique_id}"


class SavedPin(models.Model):
    pin = models.ForeignKey(Pin, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("pin", "account")

    def __str__(self):
        return f"{self.pin} saved by {self.account}"
