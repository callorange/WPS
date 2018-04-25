import functools
from io import BytesIO

import requests
import asyncio

from PIL import Image
from django.conf import settings
from django.contrib.gis.geoip2 import GeoIP2
from django.http import HttpResponse

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


from .serializers import RequestSerializer, GeoSearchRequestSerializer, StaticMapSerializer

__all__ = [
    'AddressSearch',
    'GeoSearch',
]


def geoip_check(request):
    g = GeoIP2()
    try:
        return g.city(request.META.get('REMOTE_ADDR', ''))
    except Exception as e:
        return None
        # return {
        #     'latitude': 37.5156778,
        #     'longitude': 127.0213856,
        #     'country_code': 'KO'
        # }


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

        if client_location:
            place_params = {
                'key': settings.GOOGLE_PLACE_KEY,
                'input': request.data["search_text"],
                'location': ','.join([str(client_location['latitude']), str(client_location['longitude'])]),
                'radius': '50000',
                'language': request.data.get("language", "ko"),
            }
        else:
            place_params = {
                'key': settings.GOOGLE_PLACE_KEY,
                'input': request.data["search_text"],
                'language': request.data.get("language", "ko"),
            }

        places = requests.get(place_url, params=place_params)
        if places.status_code == 200:

            async def fetch(place_id, num):
                params = {
                    'key': settings.GOOGLE_PLACE_KEY,
                    'placeid': place_id,
                    'language': request.data.get("language", "ko"),
                }

                a_loop = asyncio.get_event_loop()
                response = await a_loop.run_in_executor(
                    None,
                    functools.partial(
                        requests.get,
                        'https://maps.googleapis.com/maps/api/place/details/json',
                        params=params
                    )
                )
                data = response.json()
                data["num"] = num
                return data

            tasks = []

            for i, place in enumerate(places.json()["predictions"][:3]):
                tasks.append(fetch(place['place_id'], i))

            loop = asyncio.SelectorEventLoop()
            asyncio.set_event_loop(loop)
            r1, r2 = loop.run_until_complete(asyncio.wait(tasks))
            loop.close()

            place_list = ['' for a in range(0, i+1)]
            for t in r1:
                place_detail_json = t.result()
                place_list[place_detail_json["num"]] = {
                    "name": place_detail_json["result"]["name"],
                    "place_id": place_detail_json["result"]["place_id"],
                    "vicinity": place_detail_json["result"].get("vicinity", ""),
                    "address_components": place_detail_json["result"]["address_components"],
                    "formatted_address": place_detail_json["result"]["formatted_address"],
                    "geometry": place_detail_json["result"]["geometry"]["location"],
                }

            return place_list
        return []


class GeoSearch(APIView):

    def post(self, request, format=None):
        serializer = GeoSearchRequestSerializer(data=request.data)

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

        place_params = {
            'key': settings.GOOGLE_PLACE_KEY,
            'location': ','.join([str(client_location['latitude']), str(client_location['longitude'])]),
            'radius': '50000',
            'rankyby': 'distance',
            'keyword': request.data["search_text"],
            'language': request.data.get("language", "ko"),
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


class StaticMap(APIView):

    def get(self, request, format=None):
        serializer = StaticMapSerializer(data=request.query_params)

        if serializer.is_valid():
            google_url = 'https://maps.googleapis.com/maps/api/staticmap'
            params = {
                'key': settings.GOOGLE_PLACE_KEY,
                'center': ','.join([str(serializer.validated_data['lat']), str(serializer.validated_data['lng'])]),
                'language': 'ko',
                'zoom': 15,
                'size': '144x144',
                'format': 'jpg',
                'scale': 2,
                'markers': 'size:mid|' + ','.join([str(serializer.validated_data['lat']), str(serializer.validated_data['lng'])])
            }
            response = requests.get(google_url, params=params)

            if response.status_code == 200:
                return HttpResponse(response.content, status=status.HTTP_200_OK, content_type="image/jpeg")
            return Response(Image.open(BytesIO(response.content)), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

