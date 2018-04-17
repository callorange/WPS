# Generated by Django 2.0.3 on 2018-04-17 03:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.SmallIntegerField(max_length=1)),
                ('title', models.CharField(blank=True, max_length=200, null=True)),
                ('sub_title', models.CharField(blank=True, max_length=200, null=True)),
                ('content', models.TextField(blank=True, null=True)),
                ('img_banner', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'ordering': ['order'],
            },
        ),
    ]