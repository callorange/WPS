# Generated by Django 2.0.3 on 2018-04-23 03:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0005_auto_20180423_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_cancel_at',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]