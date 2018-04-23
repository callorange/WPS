from django.contrib.auth.models import AbstractUser
from django.db import models

from restaurant.models import Restaurant


class User(AbstractUser):
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    img_profile = models.ImageField(blank=True, upload_to='user')
    like_restaurants = models.ManyToManyField(Restaurant, related_name='like_users', verbose_name="자주찾는 식당", blank=True)
