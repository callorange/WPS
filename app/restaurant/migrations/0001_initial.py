# Generated by Django 2.0.3 on 2018-04-12 11:38

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FoodCategory',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50, null=True, verbose_name='카테고리명')),
                ('logo_url', models.CharField(blank=True, max_length=200, null=True, verbose_name='카테고리 이미지')),
            ],
            options={
                'verbose_name': '식당 카테고리',
                'verbose_name_plural': '식당 카테고리들',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='ItemCustomizationOptions',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
                ('price', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='ItemCustomizations',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
                ('min_permitted', models.PositiveSmallIntegerField(default=0)),
                ('max_permitted', models.PositiveSmallIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=200, null=True, verbose_name='이름')),
                ('description', models.CharField(blank=True, max_length=1000, null=True, verbose_name='설명')),
                ('disable_description', models.BooleanField(default=False, verbose_name='설명 노출여부')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='가격')),
                ('image_url', models.CharField(blank=True, default='', max_length=200, verbose_name='상품 이미지')),
                ('alcoholic_items', models.PositiveSmallIntegerField(default=0, verbose_name='알콜여부')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='')),
            ],
            options={
                'verbose_name': '식당 상품',
                'verbose_name_plural': '식당 상품들',
                'ordering': ['restaurant', 'section__ascending', 'created_at'],
            },
        ),
        migrations.CreateModel(
            name='MenuSections',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=500, verbose_name='메뉴명')),
                ('ascending', models.PositiveSmallIntegerField(default=0, verbose_name='메뉴 출력 순서')),
            ],
            options={
                'verbose_name': '식당 메뉴',
                'verbose_name_plural': '식당 메뉴들',
                'ordering': ['restaurant', '-ascending'],
            },
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(blank=True, max_length=100, null=True, verbose_name='이름')),
                ('parent_chain_deprecated', models.CharField(blank=True, default='', max_length=100, verbose_name='체인')),
                ('r_status', models.CharField(blank=True, max_length=10, null=True, verbose_name='상태')),
                ('r_visible', models.BooleanField(default=False, verbose_name='검색 노출 여부')),
                ('schedule_order', models.BooleanField(default=False, verbose_name='에약 가능 여부')),
                ('address1', models.CharField(blank=True, max_length=100, null=True, verbose_name='주소1')),
                ('apt_suite', models.CharField(blank=True, max_length=100, null=True, verbose_name='아파트/호수')),
                ('city', models.CharField(blank=True, max_length=20, null=True, verbose_name='시')),
                ('country', models.CharField(blank=True, max_length=10, null=True, verbose_name='국가코')),
                ('postal_code', models.CharField(blank=True, max_length=10, null=True, verbose_name='우편번호')),
                ('region', models.CharField(blank=True, max_length=10, null=True, verbose_name='주/도')),
                ('formatted_address', models.CharField(blank=True, max_length=200, null=True, verbose_name='긴 주소')),
                ('latitude', models.FloatField(blank=True, null=True, verbose_name='위도')),
                ('longtitude', models.FloatField(blank=True, null=True, verbose_name='경도')),
                ('geo_point', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326, verbose_name='Geometry')),
                ('rating', models.DecimalField(decimal_places=1, default=0, max_digits=2)),
                ('tags', models.ManyToManyField(related_name='restaurant', to='restaurant.FoodCategory', verbose_name='식당 카테고리')),
            ],
            options={
                'verbose_name': '식당',
                'verbose_name_plural': '식당들',
                'ordering': ['uuid', 'title'],
            },
        ),
        migrations.CreateModel(
            name='RestaurantContact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('public_phone_number', models.CharField(blank=True, max_length=50, null=True, verbose_name='전화번호')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contact', to='restaurant.Restaurant')),
            ],
            options={
                'verbose_name': '식당 연락처',
                'verbose_name_plural': '식당 연락처들',
                'ordering': ['restaurant', 'public_phone_number'],
            },
        ),
        migrations.CreateModel(
            name='RestaurantLogo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(blank=True, max_length=200, null=True, verbose_name='이미지 URL')),
                ('width', models.SmallIntegerField(default=0, verbose_name='넓이')),
                ('height', models.SmallIntegerField(default=0, verbose_name='높이')),
                ('is_default', models.BooleanField(default=False, help_text='식당 이미지가 여러개일 경우 기본값', verbose_name='기본 이미지')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='logos', to='restaurant.Restaurant', verbose_name='식당')),
            ],
            options={
                'verbose_name': '식당 이미지',
                'verbose_name_plural': '식당 이미지들',
                'ordering': ['restaurant', 'width'],
            },
        ),
        migrations.CreateModel(
            name='RestaurantSectionHours',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_of_week', models.CharField(choices=[('0', 'Sunday'), ('1', 'Monday'), ('2', 'Tuesday'), ('3', 'Wednesday'), ('4', 'Thursday'), ('5', 'Friday'), ('6', 'Saturday')], max_length=1, verbose_name='요일')),
                ('start_time', models.PositiveSmallIntegerField(help_text='0시 기준 분단위', verbose_name='영업시작')),
                ('end_time', models.PositiveSmallIntegerField(help_text='0시 기준 분단위', verbose_name='영업종료')),
                ('restaurant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='open_time', to='restaurant.Restaurant', verbose_name='식당')),
            ],
            options={
                'verbose_name': '식당 영업시간',
                'verbose_name_plural': '식당 영업시간들',
                'ordering': ['restaurant', 'day_of_week', 'start_time'],
            },
        ),
        migrations.CreateModel(
            name='ServiceCity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=500, null=True, verbose_name='도시명')),
                ('slug', models.SlugField(blank=True, verbose_name='도시명-slug')),
                ('lat', models.FloatField(blank=True, null=True, verbose_name='위도')),
                ('lng', models.FloatField(blank=True, null=True, verbose_name='경도')),
                ('timezone', models.CharField(blank=True, max_length=50, null=True, verbose_name='타임존')),
                ('price_format', models.CharField(blank=True, max_length=10, null=True, verbose_name='통화형식')),
                ('currency_decimal_separator', models.CharField(blank=True, default='.', max_length=1, verbose_name='통화 소수 구분 기호')),
                ('currency_num_digits_after_decimal', models.PositiveSmallIntegerField(blank=True, default=0, verbose_name='통화 소수 자리')),
                ('currency_code', models.CharField(blank=True, max_length=10, null=True, verbose_name='통화 코드')),
            ],
            options={
                'verbose_name': '서비스 도시',
                'verbose_name_plural': '서비스 도시들',
                'ordering': ['name'],
            },
        ),
        migrations.AddField(
            model_name='menusections',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='menu_section', to='restaurant.Restaurant', verbose_name='식당'),
        ),
        migrations.AddField(
            model_name='items',
            name='restaurant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='restaurant.Restaurant', verbose_name='식당'),
        ),
        migrations.AddField(
            model_name='items',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='restaurant.MenuSections', verbose_name='메뉴'),
        ),
        migrations.AddField(
            model_name='itemcustomizations',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customizations', to='restaurant.Items'),
        ),
        migrations.AddField(
            model_name='itemcustomizationoptions',
            name='customization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='options', to='restaurant.ItemCustomizations'),
        ),
    ]
