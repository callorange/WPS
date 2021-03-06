# Generated by Django 2.0.3 on 2018-04-19 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_making_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_date_time',
            field=models.DateTimeField(blank=True, default=None, null=True, verbose_name='예약시간'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('A', '준비중'), ('B', '조리중'), ('C', '배달중'), ('D', '배달완료'), ('F', '주문완료'), ('Z', '주문취소')], default='A', max_length=1, verbose_name='주문상태'),
        ),
    ]
