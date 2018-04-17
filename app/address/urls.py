from django.urls import path

from . import views

app_name = 'address'
urlpatterns = [
    path('', views.AddressSearch.as_view(), name='search'),
    path('geo/', views.GeoSearch.as_view(), name='geo-search'),
    path('map/', views.StaticMap.as_view(), name='static-map')
]