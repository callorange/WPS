from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    img_profile = models.ImageField(blank=True)
