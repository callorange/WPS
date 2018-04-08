from django.urls import path

from .apis import Restaurant

app_name = 'restaurant'

urlpatterns = [
    path('', Restaurant.as_view(), name="list")
]