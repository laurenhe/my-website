# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2018-04-20 19:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20180420_1211'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='email',
            field=models.CharField(max_length=200),
        ),
    ]
