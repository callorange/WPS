from django.urls import path

from .apis import OrderCreateView

app_name = 'order'

urlpatterns = [
    path('payment/', OrderCreateView.as_view(), name="payment"),
]
