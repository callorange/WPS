from django.contrib import admin

from .models import OrderItems, Order

admin.site.register(Order)
admin.site.register(OrderItems)
