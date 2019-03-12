# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-03-12 18:39
from __future__ import unicode_literals

import clickgestion.cash_desk.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CashClose',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(default=clickgestion.cash_desk.models.get_new_cashclose_code, editable=False, max_length=32, unique=True, verbose_name='Code')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('notes', models.TextField(blank=True, max_length=1024, null=True, verbose_name='Notes')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'Cash Desk Closure',
                'verbose_name_plural': 'Cash Desk Closures',
            },
        ),
    ]
