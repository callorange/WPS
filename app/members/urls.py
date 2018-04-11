

from django.urls import path

from .apis import UserCreate, UserListView

urlpatterns = [
    path('', UserListView.as_view()),
    path('user/', UserCreate.as_view()),

]