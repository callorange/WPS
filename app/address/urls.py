from django.urls import path, include

from . import views

app_name = 'address'
urlpatterns = [
    path('', views.AddressSearch.as_view(), name='search')
]