# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-04-18 17:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20190416_2012'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='sharecnt',
            field=models.IntegerField(default=0),
        ),
    ]
