from django.core.management.base import BaseCommand, CommandError

from ...models import ServiceCity, Restaurant
from ...crawler.ubereats import UbereatsCrawler


class Command(BaseCommand):
    help = 'ubereats에서 데이터를 가져옵니다.'

    def handle(self, *args, **options):
        u = UbereatsCrawler()
        u.get_service_cities()
        u.get_csrf_token()

        # Seoul
        # "latitude":37.524124,
        # "longitude":127.022883,
        ServiceCity.objects.filter(name='Seoul').update(lat=37.524124, lng=127.022883)

        search_city = ServiceCity.objects.filter(name='Seoul')

        # # 서대문구 신촌동
        # # "latitude":37.560519,
        # # "longitude":126.943155,
        # search_city.lat = 37.560519
        # search_city.lng = 126.943155
        # u.get_restaurant_list(search_city)
        #
        # # 마포구 성산1동
        # # "latitude":37.560519,
        # # "longitude":126.915177,
        # search_city.lat = 37.560519
        # search_city.lng = 126.915177
        # u.get_restaurant_list(search_city)
        #
        # # 마포구 동교동
        # # "latitude":37.557539,
        # # "longitude":126.926870,
        # search_city.lat = 37.557539
        # search_city.lng = 126.926870
        # u.get_restaurant_list(search_city)
        #
        # # 용산구 동빙고동
        # # "latitude":37.527243,
        # # "longitude":126.991386,
        # search_city.lat = 37.527243
        # search_city.lng = 126.991386
        # u.get_restaurant_list(search_city)
        #
        # # 용산구 한남동
        # # "latitude":37.540078,
        # # "longitude":126.999474,
        # search_city.lat = 37.540078
        # search_city.lng = 126.999474
        # u.get_restaurant_list(search_city)
        #
        # # 서초구 반포 4동
        # # "latitude":37.498555,
        # # "longitude":126.996399,
        # search_city.lat = 37.498555
        # search_city.lng = 126.996399
        # u.get_restaurant_list(search_city)
        #
        # # 강남구 신사동
        # # "latitude":37.516130,
        # # "longitude":127.019310,
        # search_city.lat = 37.516130
        # search_city.lng = 127.019310
        # u.get_restaurant_list(search_city)
        #
        # # 강남구 논현2동
        # # "latitude":37.516929,
        # # "longitude":127.040961,
        # search_city.lat = 37.516929
        # search_city.lng = 127.040961
        # u.get_restaurant_list(search_city)
        #
        # # 서초구 서초4동
        # # "latitude":37.498355,
        # # "longitude":127.027366,
        # search_city.lat = 37.498355
        # search_city.lng = 127.027366
        # u.get_restaurant_list(search_city)
        #
        # # 서초구 강남대로
        # # "latitude":37.484712,
        # # "longitude":127.034667,
        # search_city.lat = 37.484712
        # search_city.lng = 127.034667
        # u.get_restaurant_list(search_city)
        #
        # # 강남구 도곡2동
        # # "latitude":37.494760,
        # # "longitude":127.051284,
        # search_city.lat = 37.494760
        # search_city.lng = 127.051284
        # u.get_restaurant_list(search_city)
        #
        # # 관악구 행운동
        # # "latitude":37.480976,
        # # "longitude":126.956369,
        # search_city.lat = 37.480976
        # search_city.lng = 126.956369
        # u.get_restaurant_list(search_city)
        #
        # # 관악구 신림동
        # # "latitude":37.485770,
        # # "longitude":126.930689,
        # search_city.lat = 37.485770
        # search_city.lng = 126.930689
        # u.get_restaurant_list(search_city)

        u.get_restaurant_detail(Restaurant.objects.all())
        u.del_category_logo_null()
