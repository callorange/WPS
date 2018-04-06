from django.contrib.auth.models import AbstractUser
from django.db import models

from .fields import DefaultStaticImageField


class User(AbstractUser):
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    img_profile = DefaultStaticImageField(upload_to='user', blank=True)
