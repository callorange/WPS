from django.urls import path

from . import views

app_name = 'address'
urlpatterns = [
    path('', views.AddressSearch.as_view(), name='search')
]