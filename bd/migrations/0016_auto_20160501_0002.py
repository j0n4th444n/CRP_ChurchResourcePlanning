# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-05-01 04:02
from __future__ import unicode_literals

import bd.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bd', '0015_auto_20160424_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='charge',
            name='members',
            field=models.ManyToManyField(to='bd.Member', verbose_name='ocupan el cargo:'),
        ),
        migrations.AlterField(
            model_name='institution',
            name='phone',
            field=models.CharField(max_length=32, validators=[bd.models.PhoneValidator], verbose_name='tel\xe9fono'),
        ),
        migrations.AlterField(
            model_name='member',
            name='address',
            field=models.CharField(max_length=128, verbose_name='direci\xf3n'),
        ),
        migrations.AlterField(
            model_name='member',
            name='level',
            field=models.CharField(choices=[('inferior', 'Inferior'), ('primario', 'Primario'), ('secundario', 'Secundario'), ('preuniversitario', 'Preuniversitario'), ('universitario', 'Universitario'), ('master', 'Master'), ('doctor', 'Doctor')], max_length=65, verbose_name='nivel educacional'),
        ),
        migrations.AlterField(
            model_name='member',
            name='phone',
            field=models.CharField(blank=True, max_length=32, validators=[bd.models.PhoneValidator], verbose_name='tel\xe9fono'),
        ),
        migrations.AlterField(
            model_name='moneytransaction',
            name='status',
            field=models.BooleanField(default=False, verbose_name='estado'),
        ),
    ]