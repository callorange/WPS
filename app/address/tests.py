import json

from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase
from . import views


class AddressSearch(APITestCase):
    VIEW = views.AddressSearch
    URL_PATH = '/api/address/'
    URL_NAME = 'address:search'

    def test_url(self):
        """
        주소 검색 URL과 URL Name이 정상적으로 할당 되었는지 체크한다.
        :return:
        """
        reverse_url = reverse(self.URL_NAME)
        self.assertEqual(self.URL_PATH, reverse_url, 'Address Search API: URL_NAME')

        resolve_view = resolve(self.URL_PATH)
        self.assertEqual(self.URL_NAME, resolve_view.view_name, 'Address Search API: URL_PATH')

        self.assertEqual(self.VIEW.as_view().__name__, resolve_view.func.__name__, 'Address Search API: View Class')

    def test_address_search(self):
        """
        주소 검색 기능을 테스트 한다.
        :return:
        """

        # 검색 문자열을 제대로 보냈을때
        req_body = {
            "search_text": "신사",
        }
        response = self.client.post(self.URL_PATH, data=json.dumps(req_body), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('"search_text":"신사"', response.content.decode("utf-8"))

        # 검색 문자열이 비었을 때
        # req_body = {
        #     "search_text": "",
        # }
        # response = self.client.post(self.URL_PATH, data=json.dumps(req_body), content_type='application/json')
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(response.content.decode("utf-8"), '{"search_text":["This field may not be blank."]}')

        # 검색 문자열이 1글자 일때
        # req_body = {
        #     "search_text": "1",
        # }
        # response = self.client.post(self.URL_PATH, data=json.dumps(req_body), content_type='application/json')
        # self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # self.assertEqual(
        #     response.content.decode("utf-8"),
        #     '{"search_text":["Ensure this field has at least 2 characters."]}'
        # )

class GeoSearch(APITestCase):
    VIEW = views.GeoSearch
    URL_PATH = '/api/address/geo/'
    URL_NAME = 'address:geo-search'

    def test_url(self):
        """
        주소 검색 URL과 URL Name이 정상적으로 할당 되었는지 체크한다.
        :return:
        """
        reverse_url = reverse(self.URL_NAME)
        self.assertEqual(self.URL_PATH, reverse_url, 'Geo Search API: URL_NAME')

        resolve_view = resolve(self.URL_PATH)
        self.assertEqual(self.URL_NAME, resolve_view.view_name, 'Geo Search API: URL_PATH')

        self.assertEqual(self.VIEW.as_view().__name__, resolve_view.func.__name__, 'Geo Search API: View Class')

    def test_geo_search(self):
        """
        주소 검색 기능을 테스트 한다.
        :return:
        """

        # 검색 문자열을 제대로 보냈을때
        req_body = {
            "search_text": "신사",
        }
        response = self.client.post(self.URL_PATH, data=json.dumps(req_body), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('"search_text":"신사"', response.content.decode("utf-8"))
