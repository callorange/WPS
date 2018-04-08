from django.urls import path

from .apis import Restaurant, FoodCategoryView

app_name = 'restaurant'

urlpatterns = [
    path('', Restaurant.as_view(), name="list"),
    path('category/', FoodCategoryView.as_view(), name="category-list")
]