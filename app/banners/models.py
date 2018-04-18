from django.db import models


class Banner(models.Model):
    order = models.PositiveSmallIntegerField(unique=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    sub_title = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    img_banner = models.ImageField(upload_to='banner', blank=True)
    img_banner_url = models.CharField(max_length=200, blank=True, null=True)
    restaurant = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.order

    class Meta:
        ordering = ['order']
