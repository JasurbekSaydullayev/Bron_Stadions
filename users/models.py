from django.contrib.auth.models import AbstractUser
from django.db import models
from .manager import UserManager

user_types = (
    ('Admin', 'Admin'),
    ('customer', 'customer'),
    ('owner', 'owner'),
)


class User(AbstractUser):
    phone_number = models.CharField(max_length=25, unique=True)
    type = models.CharField(max_length=25, choices=user_types, default='customer')

    username = None

    USERNAME_FIELD = 'phone_number'
    objects = UserManager()

    def __str__(self):
        return self.phone_number
