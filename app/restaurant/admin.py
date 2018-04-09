from django.contrib import admin
from .models import Restaurant, RestaurantContact, FoodCategory, RestaurantLogo, ServiceCity, RestaurantSectionHours, \
    MenuSections, Items

admin.site.register(ServiceCity)

admin.site.register(FoodCategory)

admin.site.register(Restaurant)
admin.site.register(RestaurantLogo)
admin.site.register(RestaurantContact)
admin.site.register(RestaurantSectionHours)
admin.site.register(MenuSections)
admin.site.register(Items)
