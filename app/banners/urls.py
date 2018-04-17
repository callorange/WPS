from django.urls import path

from .apis import BannerListCreateView

urlpatterns = [
    path('', BannerListCreateView.as_view()),
]
