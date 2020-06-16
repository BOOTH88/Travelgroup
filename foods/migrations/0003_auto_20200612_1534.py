# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2020-06-12 15:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foods', '0002_auto_20200604_1524'),
    ]

    operations = [
        migrations.RenameField(
            model_name='food',
            old_name='username',
            new_name='foodie',
        ),
        migrations.AlterField(
            model_name='food',
            name='info',
            field=models.CharField(max_length=90, verbose_name='文章简介'),
        ),
    ]