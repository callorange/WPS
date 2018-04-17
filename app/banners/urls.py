from django.urls import path

from .apis import BannerListCreateView, BannerRetrieveUpdateView

urlpatterns = [
    path('', BannerListCreateView.as_view()),
    path('<int:order>/', BannerRetrieveUpdateView.as_view()),
]
