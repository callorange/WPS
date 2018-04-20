from io import BytesIO

import requests

from PIL import Image
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import status


def index(request):
    return render(request, 'index.html')


def static_directions(request):
    google_url = 'https://maps.googleapis.com/maps/api/directions/json'
    params = {
        'key': settings.GOOGLE_PLACE_KEY,
        'origin': '37.494760,127.051284',
        'destination': '37.495760,127.052284',
        # 'path': 'color:0x0000ff|weight:5|40.737102,-73.990318|40.749825,-73.987963|40.752946,-73.987384|40.755823,-73.986397',
        'mode': 'drive',
        # 'language': 'ko',
        # 'size': '800x800',
        'format': 'jpg',
    }
    response = requests.get(google_url, params=params)
    print(response.url)

    if response.status_code == 200:
        return HttpResponse(response.content, status=200, content_type="image/jpeg")


https://maps.googleapis.com/maps/api/directions/json?origin=75+9th+Ave+New+York,+NY&destination=MetLife+Stadium+1+MetLife+Stadium+Dr+East+Rutherford,+NJ+07073&key=AIzaSyDzHITjM5g2MqpYwOzvA0zb9BuKOImwpx4