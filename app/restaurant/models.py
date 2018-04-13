import uuid

from django.contrib.gis.db import models
from django.db.models import Max


class ServiceCity(models.Model):
    name = models.CharField(blank=True, null=True, max_length=500, verbose_name="도시명",)
    slug = models.SlugField(blank=True, max_length=50, verbose_name="도시명-slug")
    lat = models.FloatField(blank=True, null=True, verbose_name="위도",)
    lng = models.FloatField(blank=True, null=True, verbose_name="경도",)
    timezone = models.CharField(blank=True, null=True, max_length=50, verbose_name="타임존",)
    price_format = models.CharField(blank=True, null=True, max_length=10, verbose_name="통화형식",)
    currency_decimal_separator = models.CharField(blank=True, max_length=1, default='.', verbose_name="통화 소수 구분 기호",)
    currency_num_digits_after_decimal = models.PositiveSmallIntegerField(blank=True, default=0, verbose_name="통화 소수 자리",)
    currency_code = models.CharField(blank=True, null=True, max_length=10, verbose_name="통화 코드",)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '서비스 도시'
        verbose_name_plural = '서비스 도시들'
        ordering = ['name']


class FoodCategory(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4,)
    name = models.CharField(blank=True, null=True, max_length=50, verbose_name="카테고리명",)
    logo_url = models.CharField(blank=True, null=True, max_length=200, verbose_name="카테고리 이미지",)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '식당 카테고리'
        verbose_name_plural = '식당 카테고리들'
        ordering = ['name']


class Restaurant(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(blank=True, null=True, max_length=100, verbose_name="이름")
    parent_chain_deprecated = models.CharField(blank=True, default='', max_length=100, verbose_name="체인",)

    r_status = models.CharField(blank=True, null=True, max_length=10, verbose_name="상태",)
    r_visible = models.BooleanField(default=False, verbose_name="검색 노출 여부",)
    schedule_order = models.BooleanField(default=False, verbose_name="에약 가능 여부",)

    address1 = models.CharField(blank=True, null=True, max_length=100, verbose_name="주소1",)
    apt_suite = models.CharField(blank=True, null=True, max_length=100, verbose_name="아파트/호수",)
    city = models.CharField(blank=True, null=True, max_length=20, verbose_name="시",)
    country = models.CharField(blank=True, null=True, max_length=10, verbose_name="국가코",)
    postal_code = models.CharField(blank=True, null=True, max_length=10, verbose_name="우편번호",)
    region = models.CharField(blank=True, null=True, max_length=10, verbose_name="주/도",)
    formatted_address = models.CharField(blank=True, null=True, max_length=200, verbose_name="긴 주소",)

    latitude = models.FloatField(blank=True, null=True, verbose_name="위도",)
    longtitude = models.FloatField(blank=True, null=True, verbose_name="경도",)
    geo_point = models.PointField(srid=4326, verbose_name="Geometry", null=True)

    tags = models.ManyToManyField(FoodCategory, related_name="restaurant", verbose_name="식당 카테고리")

    rating = models.DecimalField(max_digits=2, decimal_places=1, default=0)

    def __str__(self):
        return f'{self.title} - {self.address1}'

    class Meta:
        verbose_name = '식당'
        verbose_name_plural = '식당들'
        ordering = ['uuid', 'title']


class RestaurantLogo(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="logos", verbose_name="식당",)
    url = models.CharField(blank=True, null=True, max_length=200, verbose_name="이미지 URL",)
    width = models.SmallIntegerField(default=0, verbose_name="넓이",)
    height = models.SmallIntegerField(default=0, verbose_name="높이",)
    is_default = models.BooleanField(default=False, verbose_name="기본 이미지", help_text="식당 이미지가 여러개일 경우 기본값")

    def __str__(self):
        return "{} - {}".format(self.restaurant.title, self.url)

    class Meta:
        ordering = ['restaurant', 'width']
        verbose_name = '식당 이미지'
        verbose_name_plural = '식당 이미지들'


class RestaurantContact(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="contact")
    public_phone_number = models.CharField(blank=True, null=True, max_length=50, verbose_name="전화번호",)

    def __str__(self):
        return self.public_phone_number

    class Meta:
        ordering = ['restaurant', 'public_phone_number']
        verbose_name = '식당 연락처'
        verbose_name_plural = '식당 연락처들'


class RestaurantSectionHours(models.Model):
    DAYS_OF_WEEK = (
        ('0', 'Sunday'),
        ('1', 'Monday'),
        ('2', 'Tuesday'),
        ('3', 'Wednesday'),
        ('4', 'Thursday'),
        ('5', 'Friday'),
        ('6', 'Saturday'),
        # ('7', 'Everyday'),
    )
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="open_time", verbose_name="식당",)
    day_of_week = models.CharField(max_length=1, choices=DAYS_OF_WEEK, verbose_name="요일")
    start_time = models.PositiveSmallIntegerField(verbose_name="영업시작", help_text="0시 기준 분단위")
    end_time = models.PositiveSmallIntegerField(verbose_name="영업종료", help_text="0시 기준 분단위")

    def __str__(self):
        return "{} - {}: {}~{}".format(self.restaurant.title, self.get_day_of_week_display(), self.start_time, self.end_time)

    class Meta:
        ordering = ['restaurant', 'day_of_week', 'start_time']
        verbose_name = '식당 영업시간'
        verbose_name_plural = '식당 영업시간들'


class MenuSections(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="menu_section", verbose_name="식당",)
    title = models.CharField(max_length=500, verbose_name="메뉴명")
    ascending = models.PositiveSmallIntegerField(default=0, verbose_name="메뉴 출력 순서")

    def __str__(self):
        return f'{self.title}'

    def save(self, *args, **kwargs):
        chk = MenuSections.objects.filter(
            restaurant=self.restaurant
        )
        if chk.exists() is True:
            max_asc = chk.aggregate(Max('ascending'))
            self.ascending = max_asc['ascending__max'] + 1
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['restaurant', '-ascending']
        verbose_name = '식당 메뉴'
        verbose_name_plural = '식당 메뉴들'


class Items(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="items", verbose_name="식당")
    section = models.ForeignKey(MenuSections, on_delete=models.CASCADE, related_name="items", verbose_name="메뉴")

    title = models.CharField(blank=True, null=True, max_length=200, verbose_name="이름")
    description = models.CharField(blank=True, null=True, max_length=1000, verbose_name="설명")
    disable_description = models.BooleanField(default=False, verbose_name="설명 노출여부")
    price = models.PositiveIntegerField(default=0, verbose_name="가격")
    image_url = models.CharField(blank=True, default='', max_length=200, verbose_name="상품 이미지")
    alcoholic_items = models.PositiveSmallIntegerField(default=0, verbose_name='알콜여부')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        ordering = ['restaurant', 'section__ascending', 'created_at']
        verbose_name = '식당 상품'
        verbose_name_plural = '식당 상품들'


class ItemCustomizations(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    item = models.ForeignKey(Items, on_delete=models.CASCADE, related_name="customizations")
    title = models.CharField(blank=True, null=True, max_length=500)
    min_permitted = models.PositiveSmallIntegerField(default=0)
    max_permitted = models.PositiveSmallIntegerField(default=0)


class ItemCustomizationOptions(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)
    customization = models.ForeignKey(ItemCustomizations, on_delete=models.CASCADE, related_name="options")
    title = models.CharField(blank=True, null=True, max_length=500)
    price = models.PositiveSmallIntegerField(default=0)
