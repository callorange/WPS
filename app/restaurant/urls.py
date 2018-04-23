from django.urls import path

from .apis import FoodCategoryView, RestaurantView, RestaurantMenuView, RestaurantInfoView, RestaurantMenuItemView, \
    RestaurantMenuInfoView, RestaurantLikeView

app_name = 'restaurant'


urlpatterns = [
    path('item/<slug:item>/', RestaurantMenuItemView.as_view(), name="item-info"),

    path('menu/<slug:menu>/', RestaurantMenuInfoView.as_view(), name="menu-info"),
    path('<slug:restaurant>/menu/', RestaurantMenuView.as_view(), name="menu-list"),

    path('category/', FoodCategoryView.as_view(), name="category-list"),

    path('<slug:restaurant>/like/', RestaurantLikeView.as_view(), name="like"),
    path('<slug:restaurant>/', RestaurantInfoView.as_view(), name="info"),
    path('', RestaurantView.as_view(), name="list"),
]
