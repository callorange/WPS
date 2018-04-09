from django.contrib.gis.geos import GEOSGeometry, Point
from django.contrib.gis.measure import D
from rest_framework.test import APITestCase

from restaurant.models import Restaurant


class AddressSearch(APITestCase):

    def test_point_search(self):

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
