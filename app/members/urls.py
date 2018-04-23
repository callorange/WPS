from django.urls import path

from .apis import UserCreate, UserListView, UserDetail, UserLikeRestaurants

urlpatterns = [
    path('', UserListView.as_view()),
    path('user/', UserCreate.as_view()),
    path('user/<int:pk>/', UserDetail.as_view()),
    path('user/<int:pk>/like_restaurants/', UserLikeRestaurants.as_view()),
]
