from django.urls import path

from .apis import UserCreate

urlpatterns = [
    path('user/', UserCreate.as_view())

]