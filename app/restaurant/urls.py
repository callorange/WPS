from django.urls import path

from .apis import FoodCategoryView, RestaurantView, RestaurantMenuView, RestaurantInfoView, RestaurantMenuItemView

app_name = 'restaurant'


urlpatterns = [
    path('<slug:restaurant>/menu/<slug:item>/', RestaurantMenuItemView.as_view(), name="menu-list"),
    path('<slug:restaurant>/menu/', RestaurantMenuView.as_view(), name="menu-list"),
    path('category/', FoodCategoryView.as_view(), name="category-list"),

    path('<slug:restaurant>/', RestaurantInfoView.as_view(), name="info"),
    path('', RestaurantView.as_view(), name="list"),
]
