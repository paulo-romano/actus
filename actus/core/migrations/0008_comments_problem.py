# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-03 15:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20161203_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='problem',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='core.Problem'),
            preserve_default=False,
        ),
    ]
