from django.db import models


class Banner(models.Model):
    order = models.SmallIntegerField()
    title = models.CharField(max_length=200, blank=True, null=True)
    sub_title = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    img_banner = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.order

    class Meta:
        ordering = ['order']
