# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-24 20:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bd', '0014_song_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='video',
            field=models.FileField(null=True, upload_to='videosTutoriales', verbose_name='videotutoriales'),
        ),
    ]