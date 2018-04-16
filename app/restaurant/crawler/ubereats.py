import asyncio
import functools
import json
import traceback
from io import BytesIO
from uuid import UUID

import requests
from PIL import Image
from django.contrib.gis.geos import Point
from django.utils.text import slugify

from ..models import ServiceCity, Restaurant, FoodCategory, RestaurantLogo, RestaurantContact, RestaurantSectionHours, \
    MenuSections, Items

__all__ = [
    'UbereatsCrawler',
]


class UbereatsCrawler():
    UBEREATS_DOMAIN = 'https://www.ubereats.com/'
    CSRF_TOKEN = ''

    def __init__(self):
        print("ubereats에서 데이터를 가져옵니다")
        self.req = requests.Session()

    def get_csrf_token(self):
        response = self.req.get(self.UBEREATS_DOMAIN)
        if response.status_code == 200:
            self.CSRF_TOKEN = response.headers['x-csrf-token']
        else:
            raise ValueError

    def get_service_cities(self):
        """
        서비스 도시 목록을 DB에 저장한다.
        """
        def get_city_id(city):
            return city["cityId"]

        print("# Service Cities Job:")

        search_url = 'https://www.ubereats.com/rtapi/eats/v1/get-service-cities'
        response = self.req.get(search_url)

        if response.status_code == 200:
            res_json = response.json()
            cities = res_json["serviceCities"]
            cities = sorted(cities, key=get_city_id)

            add = 0
            mod = 0
            for city in cities:
                print(city)
                cityName = city["cityName"]
                cityLat = city.get("cityLat", city.get("lat", ''))
                cityLng = city.get("cityLng", city.get("lng", ''))
                slug = slugify(cityName) #city.get("slug", cityName)
                city_obj, created = ServiceCity.objects.get_or_create(
                    name=cityName,
                )
                if created is False:
                    city_obj.name = cityName
                    city_obj.lat = float(cityLat)
                    city_obj.lng = float(cityLng)
                    city_obj.slug = slug
                    city_obj.save()
                    mod += 1
                else:
                    add += 1

            print(f"    ** Service Cities Add End - target: {len(cities)}(add: {add}, mod: {mod})")
        else:
            raise ValueError

    def get_restaurant_list(self, cities):
        """
        음식점 목록을 DB에 저장한다.
        """
        print("# Service restaurant Job:")

        if len(cities) is 0:
            cities = ServiceCity.objects.all()[:2]

        # seoul = ServiceCity.objects.get(name__contains="New York")

        search_categories = 'https://www.ubereats.com/rtapi/eats/v1/search/home'
        search_market_places = 'https://www.ubereats.com/rtapi/eats/v2/marketplaces'
        search_all_stores = 'https://www.ubereats.com/rtapi/eats/v1/allstores'
        search_headers = {
            'Content-Type': 'application/json',
            'x-csrf-token': self.CSRF_TOKEN,
        }
        for city in cities:
            search_data = {
                "targetLocation": {
                    # "latitude": 40.7127753,
                    # "longitude": -74.0059728,
                    # "reference": "ChIJOwg_06VPwokRYv534QaPC8g",
                    # "type": "google_places",
                    # "address":  {
                    #     "title": "New York",
                    #     "address1": "New York",
                    #     "city": "New York"
                    # }
                    "latitude": city.lat,
                    "longitude": city.lng,
                    # "reference": "ChIJzWXFYYuifDUR64Pq5LTtioU",
                    # "address":  {
                    #     "title": "Seoul",
                    #     "address1": "Seoul",
                    #     "city": "Seoul"
                    # }
                },
                "hashes": {"stores": ""},
                "feed": "combo",
                "feedTypes": ["STORE", "SEE_ALL_STORES"],
                "feedVersion": 2,
                "pageInfo": {
                    "offset": 0,
                    "pageSize": 99999
                },
                "supportedTypes": ["grid"],
            }

            print("    ** {:15} Restaurants Add".format(str(city)))

            # Marketplace에서 타임존 데이터 뽑아 오기
            response = self.req.post(search_market_places, headers=search_headers, data=json.dumps(search_data))
            if response.status_code == 200:
                res_json = response.json()
                try:
                    restaurants = res_json["marketplace"]

                    if city.timezone is None:
                        print("       ** timezone udpate")
                        city.timezone = restaurants["timezone"]
                        city.price_format = restaurants["priceFormat"]
                        city.currency_decimal_separator = restaurants["currencyDecimalSeparator"]
                        city.currency_num_digits_after_decimal = restaurants["currencyNumDigitsAfterDecimal"]
                        city.currency_code = restaurants["currencyCode"]
                        city.save()

                except Exception as e:
                    print(e)
            else:
                raise ValueError

            # 상점 정보 넣기
            print("       ** get restaurants")
            response_all = self.req.post(search_all_stores, headers=search_headers, data=json.dumps(search_data))
            # store_all에 결과가 너무 많아서 수정
            # response_all = response
            if response_all.status_code == 200:
                res_json = response_all.json()
                try:

                    # store_all로 작업하려면 위에걸로 수정
                    restaurants = res_json["feed"]["storesMap"]
                    # restaurants = res_json["marketplace"]["feed"]["storesMap"]

                    restaurant_add_num = 0
                    restaurant_mod_num = 0

                    for key, restaurant in restaurants.items():
                        print("         *{}".format(restaurant["title"]))

                        # 레스토랑을 만든다. ( 가능하면 업데이트 )
                        restaurant_obj, restaurant_created = Restaurant.objects.get_or_create(uuid=restaurant["uuid"])
                        Restaurant.objects.filter(uuid=restaurant["uuid"]).update(
                            uuid=restaurant["uuid"],
                            title=restaurant["title"],
                            parent_chain_deprecated=restaurant.get('parentChainDeprecated', ''),
                            r_status=restaurant["status"],
                            r_visible=restaurant["isStoreVisible"],
                            address1=restaurant["location"]["address"].get("address1", ""),
                            apt_suite=restaurant["location"]["address"].get("aptOrSuite", ""),
                            city=restaurant["location"]["address"].get("city", ""),
                            country=restaurant["location"]["address"].get("country", ""),
                            postal_code=restaurant["location"]["address"].get("postalCode", ""),
                            region=restaurant["location"]["address"].get("region", ""),
                            formatted_address=restaurant["location"]["address"]["formattedAddress"],
                            latitude=restaurant["location"]["latitude"],
                            longtitude=restaurant["location"]["longitude"],
                            geo_point=Point(y=restaurant["location"]["latitude"], x=restaurant["location"]["longitude"], srid=4326)
                        )

                        # 카테고리랑 태그를 만든다.
                        for tag_item in restaurant.get("tags", []):
                            tag_obj, tag_created = FoodCategory.objects.get_or_create(
                                name=tag_item["name"],
                            )
                            restaurant_obj.tags.add(tag_obj)

                        for tag_item in restaurant.get("categories", []):
                            tag_obj, tag_created = FoodCategory.objects.get_or_create(
                                name=tag_item["name"],
                            )
                            restaurant_obj.tags.add(tag_obj)


                        # 상점 이미지를 넣는다.
                        if restaurant.get("heroImage", None) and restaurant["heroImage"].get("items", None):
                            for hero_img in sorted(restaurant["heroImage"]["items"], key=sort_img_width):
                                if RestaurantLogo.objects.filter(restaurant=restaurant_obj, url=hero_img["url"]).exists() is False:
                                    RestaurantLogo.objects.create(
                                        restaurant=restaurant_obj,
                                        url=hero_img["url"],
                                        width=hero_img["width"],
                                        height=hero_img["height"],
                                    )

                        # width=550 인 이미지 기본값 True로 업데이트.
                        # 없으면 기본 이미지를 넣어준다.
                        logo_imgs = RestaurantLogo.objects.filter(restaurant=restaurant_obj, width=550)
                        if logo_imgs.exists():
                            logo_imgs.update(is_default=True)
                        else:
                            if restaurant.get("heroImageUrl", '') != '':
                                print("             * Default Logo Update!")
                                hero_image_res = requests.get(restaurant.get("heroImageUrl", ''))
                                hero_image = Image.open(BytesIO(hero_image_res.content))
                                hero_obj, hero_created = RestaurantLogo.objects.get_or_create(
                                    restaurant=restaurant_obj,
                                    url=restaurant["heroImageUrl"],
                                    width=hero_image.width,
                                    height=hero_image.height,
                                    is_default=True,
                                )
                                hero_obj.is_default = True
                                hero_obj.save()

                        # 상점 연락처
                        if restaurant.get("publicContact", None) and restaurant["publicContact"].get("publicPhoneNumber", None):
                            RestaurantContact.objects.get_or_create(
                                restaurant=restaurant_obj,
                                public_phone_number=restaurant["publicContact"]["publicPhoneNumber"],
                            )

                        # 상점 영업시간
                        for section_info in restaurant['sectionHoursInfo']:
                            for section_day in day_range(section_info['dayRange']):
                                for section_hour in section_info['sectionHours']:
                                    RestaurantSectionHours.objects.update_or_create(
                                        restaurant=restaurant_obj,
                                        day_of_week=section_day,
                                        start_time=section_hour['startTime'],
                                        end_time=section_hour['endTime'],
                                    )

                        if restaurant_created:
                            restaurant_add_num = restaurant_add_num + 1
                        else:
                            restaurant_mod_num = restaurant_mod_num + 1

                    print("         ** target: {}(add: {}, mod: {})".format(len(restaurants), restaurant_add_num, restaurant_mod_num))
                except Exception as e:
                    print(e)
                    traceback.print_exc()
            else:
                raise ValueError

            # 카테고리 정보 업데이트
            print("       ** category update")
            response_categories = self.req.post(search_categories, headers=search_headers, data=json.dumps(search_data))
            if response_categories.status_code == 200:
                res_json = response_categories.json()
                try:
                    category_list = []
                    for category_section in res_json['suggestedSections']:
                        category_list = category_list + category_section.get('gridItems', [])

                    for category_item in category_list:
                        category_title = category_item['title']
                        category_imgs = category_item.get('suggestedStoreItems', None)
                        if category_title and category_imgs:
                            if FoodCategory.objects.filter(name__contains=category_title).exists():
                                category_obj = FoodCategory.objects.filter(name__contains=category_title)
                                category_obj.update(logo_url=category_imgs[0]["imageUrl"])

                except Exception as e:
                    print(e)
            else:
                raise ValueError

    def get_restaurant_detail(self, source_stores):
        print("# Service restaurant detail Job:")

        tasks = []
        for num, store in enumerate(source_stores):
            tasks.append(self._get_restaurant_detail(store, num))

        loop = asyncio.SelectorEventLoop()
        asyncio.set_event_loop(loop)
        r1, r2 = loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

    async def _get_restaurant_detail(self, store, job_num):
        # 상점메뉴 업데이트
        search_store_info = 'https://www.ubereats.com/rtapi/eats/v2/stores/'
        search_store_info_url = search_store_info + str(store.uuid)

        a_loop = asyncio.get_event_loop()
        response = await a_loop.run_in_executor(
            None,
            functools.partial(
                requests.get,
                search_store_info_url,
            )
        )

        if response.status_code == 200:
            res_json = response.json()
            print("       ** Job Num: {:4}, Store: {}".format(job_num, store.title))
            try:
                # 메뉴 섹션
                menu_asc = 0
                for menu_key, menu_section in res_json['store']['subsectionsMap'].items():
                    menu_asc = menu_asc + 1
                    # print("         *{}".format(menu_section["title"]))
                    if "원산지" not in menu_section["title"]:
                        if MenuSections.objects.filter(uuid=menu_section['uuid']).exists() is False:
                            section_obj = MenuSections.objects.create(
                                uuid=menu_section['uuid'],
                                restaurant=store,
                                title=menu_section['title'],
                                ascending=menu_asc,
                            )

                            for menu_item in menu_section['displayItems']:
                                Items.objects.get_or_create(
                                    uuid=menu_item['uuid'],
                                    restaurant=store,
                                    section=section_obj,
                                )

                # 상품 넣기
                for menu_key, menu_item in res_json['store']['itemsMap'].items():
                    # print("         *{}".format(menu_item["title"]))
                    if Items.objects.filter(uuid=menu_item['uuid']).exists():
                        item_obj = Items.objects.get(uuid=menu_item['uuid'])
                        item_obj.title = menu_item['title']
                        item_obj.description = menu_item.get('itemDescription', '')
                        item_obj.disable_description = menu_item.get('disableItemInstructions', False)
                        item_obj.price = menu_item['price']
                        item_obj.image_url = menu_item.get('imageUrl', menu_item.get('rawImageUrl', ''))
                        item_obj.alcoholic_items = menu_item.get('alcoholicItems', 0)
                        item_obj.created_at = menu_item['createdAt']
                        item_obj.save()

            except Exception as e:
                print(e)
                traceback.print_exc()
        else:
            print('status: ', response.status_code)
            raise ValueError

    def del_category_logo_null(self):
        FoodCategory.objects.filter(logo_url__isnull=True).delete()


def sort_img_width(img):
    return img["width"]


def validate_uuid4(uuid_str):
    try:
        val = UUID(uuid_str, version=4)
        return True
    except ValueError:
        return False


def day_range(day_range):
    if day_range == "Everyday":
        return range(0, 7)

    day_dict = dict((y, int(x)) for x, y in RestaurantSectionHours.DAYS_OF_WEEK)
    if '-' in day_range:
        day_split = [day_dict[x.strip()] for x in day_range.split('-')]
        return range(day_split[0], day_split[1]+1)
    else:
        return range(day_dict[day_range], day_dict[day_range]+1)
