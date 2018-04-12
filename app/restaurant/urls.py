from django.urls import path

from .apis import FoodCategoryView, RestaurantView, RestaurantMenuView

app_name = 'restaurant'


urlpatterns = [
    path('', RestaurantView.as_view(), name="list"),
    path('<slug:restaurant>/menu/', RestaurantMenuView.as_view(), name="list"),
    path('category/', FoodCategoryView.as_view(), name="category-list")
]
