import json

from django.contrib.gis.geos import GEOSGeometry, Point
from django.contrib.gis.measure import D
from django.urls import reverse, resolve
from rest_framework import status
from rest_framework.test import APITestCase

from restaurant import apis
from restaurant.models import Restaurant, RestaurantLogo, FoodCategory


class RestaurantSearch(APITestCase):
    VIEW = apis.RestaurantView
    URL_PATH = '/api/restaurant/'
    URL_NAME = 'restaurant:list'

    def test_url(self):
        """
        레스토랑 검색 URL과 URL Name이 정상적으로 할당 되었는지 체크한다.
        :return:
        """
        reverse_url = reverse(self.URL_NAME)
        self.assertEqual(self.URL_PATH, reverse_url, 'restaurant Search API: URL_NAME')

        resolve_view = resolve(self.URL_PATH)
        self.assertEqual(self.URL_NAME, resolve_view.view_name, 'restaurant Search API: URL_PATH')
        self.assertEqual(self.VIEW.as_view().__name__, resolve_view.func.__name__, 'restaurant Search API: View Class')

    def test_point_search(self):
        """
        레스토랑 DB 모델링 확인. POINT 컬럼으로 정상 검색 되는지 테스트.
        :return:
        """

        # 신사역
        search_point = GEOSGeometry('POINT(127.019310 37.516130)', srid=4326)

        # 도곡렉슬 아파트
        r1 = Restaurant.objects.create(
            title="Test Restaurant 1",
            r_status='ACTIVE',
            r_visible=True,
            latitude=37.494760,
            longtitude=127.051284,
            geo_point=Point(y=37.494760, x=127.051284, srid=4326)
        )

        # 신사역 - 도곡렉슬 아파트: 직선거리 3.7km
        self.assertEqual(
            1,
            Restaurant.objects.filter(geo_point__distance_lte=(search_point, D(km=10))).count()
        )
        self.assertEqual(
            1,
            Restaurant.objects.filter(geo_point__distance_lte=(search_point, D(km=5))).count()
        )
        self.assertEqual(
            0,
            Restaurant.objects.filter(geo_point__distance_lte=(search_point, D(km=1))).count()
        )

    def test_restaurant_search(self):
        """
        레스토랑 검색 API테스트
        :return:
        """

        # 도곡렉슬 아파트
        r1 = Restaurant.objects.create(
            title="Test Restaurant 1",
            r_status='ACTIVE',
            r_visible=True,
            latitude=37.494760,
            longtitude=127.051284,
            geo_point=Point(y=37.494760, x=127.051284, srid=4326),
        )
        RestaurantLogo.objects.create(
            restaurant=r1,
            url='test.jpg',
            width=550,
            height=750,
        )

        # 신사역 - 도곡렉슬 아파트: 직선거리 3.7km
        req_body = {
            "lat": 37.51613,
            "lng": 127.01931,
            "radius": 3000,
        }

        response = self.client.get(self.URL_PATH, data=req_body,)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        res_json = json.loads(response.content.decode("utf-8"))

        # 3km 로 검색했으니 검색 결과가 있으면 안된다.
        self.assertEqual(0, res_json['count'])

        # 검색 파라미터가 제대로 체크 되었는지 확인
        self.assertEqual('37.51613', res_json['search_params']['lat'])
        self.assertEqual('127.01931', res_json['search_params']['lng'])
        self.assertEqual('3000', res_json['search_params']['radius'])

        # 신사역 - 도곡렉슬 아파트: 직선거리 3.7km
        req_body = {
            "lat": 37.51613,
            "lng": 127.01931,
            "radius": 4000,
            "page_size": 2,
        }

        response = self.client.get(self.URL_PATH, data=req_body,)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        res_json = json.loads(response.content.decode("utf-8"))

        # 4km 로 검색했으니 검색 결과가 있어야 한다.
        self.assertEqual(1, res_json['count'])

        # 검색 파라미터가 제대로 체크 되었는지 확인
        self.assertEqual('37.51613', res_json['search_params']['lat'])
        self.assertEqual('127.01931', res_json['search_params']['lng'])
        self.assertEqual('4000', res_json['search_params']['radius'])
        self.assertEqual('2', res_json['search_params']['page_size'])


class CategorySearch(APITestCase):
    VIEW = apis.FoodCategoryView
    URL_PATH = '/api/restaurant/category/'
    URL_NAME = 'restaurant:category-list'

    def test_url(self):
        """
        카테고리 리스트 URL과 URL Name이 정상적으로 할당 되었는지 체크한다.
        :return:
        """
        reverse_url = reverse(self.URL_NAME)
        self.assertEqual(self.URL_PATH, reverse_url, 'Category Search API: URL_NAME')

        resolve_view = resolve(self.URL_PATH)
        self.assertEqual(self.URL_NAME, resolve_view.view_name, 'Category Search API: URL_PATH')
        self.assertEqual(self.VIEW.as_view().__name__, resolve_view.func.__name__, 'Category Search API: View Class')

    def test_category_search(self):
        """
        카테고리 검색 API테스트
        :return:
        """

        response = self.client.get(self.URL_PATH,)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        res_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(0, res_json['count'])

        # 테스트 카테고리 생성
        c1 = FoodCategory.objects.create(
            name='Test Menu',
            logo_url='test.jpg',
        )

        response = self.client.get(self.URL_PATH,)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        res_json = json.loads(response.content.decode("utf-8"))
        self.assertEqual(1, res_json['count'])
