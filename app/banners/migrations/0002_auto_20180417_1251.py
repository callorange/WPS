# Generated by Django 2.0.3 on 2018-04-17 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banners', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='order',
            field=models.SmallIntegerField(),
        ),
    ]