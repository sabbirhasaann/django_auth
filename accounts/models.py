from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from .manager import UserManager


class User(AbstractUser):

    username = None
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


# class Order(models.Model):
#     user = models.ForeignKey(
#         User,
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#     )
