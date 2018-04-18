from django.urls import path

from .apis import OrderCreateView, OrderListView

app_name = 'order'

urlpatterns = [
    path('payment/', OrderCreateView.as_view(), name="payment"),

    path('list/prepare/', OrderListView.as_view(), name="list-prepare"),
    path('list/past/', OrderListView.as_view(), name="list-past"),
    path('list/', OrderListView.as_view(), name="list"),
]
