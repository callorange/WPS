import requests
from django.conf import settings

from django.contrib.gis.geoip2 import GeoIP2

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from .serializers import RequestSerializer


def geoip_check(request):
    g = GeoIP2()
    try:
        return g.city(request.META.get('REMOTE_ADDR', ''))
    except Exception as e:
        return {
            'latitude': 37.5156778,
            'longitude': 127.0213856,
            'country_code': 'KO'
        }


class AddressSearch(APIView):

    def post(self, request, format=None):
        serializer = RequestSerializer(data=request.data)

        if serializer.is_valid():
            search_result = dict(serializer.data)
            search_result.update({'result': self.place_search(request)})
            return Response(search_result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def place_search(self, request):
        # 구글 장소 자동완성 URL
        place_url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json'
        # 구글 장소 세부정보 URL
        place_detail_url = 'https://maps.googleapis.com/maps/api/place/details/json'

        client_location = geoip_check(request)

        place_params = {
            'key': settings.GOOGLE_PLACE_KEY,
            'input': request.data["search_text"],
            'location': ','.join([str(client_location['latitude']), str(client_location['longitude'])]),
            'radius': '50000',
            'language': client_location['country_code'],
        }
        place_detail_params = {
            'key': settings.GOOGLE_PLACE_KEY,
            'placeid': '',
            'language': client_location['country_code'],
        }

        places = requests.get(place_url, params=place_params)
        if places.status_code == 200:
            place_list = []
            for place in places.json()["predictions"][:5]:
                place_detail_params["placeid"] = place['place_id']
                place_detail = requests.get(place_detail_url, params=place_detail_params)
                place_detail_json = place_detail.json()
                place_list.append({
                    "name": place_detail_json["result"]["name"],
                    "place_id": place_detail_json["result"]["place_id"],
                    "vicinity": place_detail_json["result"]["vicinity"],
                    "address_components": place_detail_json["result"]["address_components"],
                    "formatted_address": place_detail_json["result"]["formatted_address"],
                    "geometry": place_detail_json["result"]["geometry"]["location"],
                })

            return place_list
        return []


class GeoSearch(APIView):

    def post(self, request, format=None):
        serializer = RequestSerializer(data=request.data)

        if serializer.is_valid():
            search_result = dict(serializer.data)
            search_result.update({'result': self.place_search(request)})
            return Response(search_result, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def place_search(self, request):
        # 구글 장소 검색 URL
        place_url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'

        if request.data.get('latitude', None) and request.data.get('longitude', None):
            client_location = {
                'latitude': request.data.get('latitude', None),
                'longitude': request.data.get('longitude', None),
                'country_code': 'KO'
            }
        else:
            client_location = geoip_check(request)

        place_params = {
            'key': settings.GOOGLE_PLACE_KEY,
            'location': ','.join([str(client_location['latitude']), str(client_location['longitude'])]),
            'radius': '50000',
            'rankyby': 'distance',
            'keyword': request.data["search_text"],
            'language': client_location['country_code'],
        }
        places = requests.get(place_url, params=place_params)
        if places.status_code == 200:
            place_list = []
            for place in places.json()["results"]:
                place_list.append({
                    "name": place["name"],
                    "place_id": place["place_id"],
                    "vicinity": place["vicinity"],
                    "geometry": place["geometry"]["location"],
                })

            return place_list
        return []

