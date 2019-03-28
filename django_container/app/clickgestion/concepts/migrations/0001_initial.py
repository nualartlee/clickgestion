# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-03-28 21:41
from __future__ import unicode_literals

import clickgestion.concepts.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('transactions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BaseConcept',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accounting_group', models.CharField(blank=True, max_length=32, null=True, verbose_name='Accounting Group')),
                ('code', models.CharField(editable=False, max_length=32, unique=True, verbose_name='Code')),
                ('concept_class', models.CharField(editable=False, max_length=32, verbose_name='Concept Class')),
                ('concept_name', models.CharField(editable=False, max_length=32, verbose_name='Concept Name')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('end_date', models.DateTimeField(blank=True, null=True, verbose_name='End Date')),
                ('start_date', models.DateTimeField(blank=True, null=True, verbose_name='Start Date')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('vat_percent', models.FloatField(verbose_name='VAT Percent')),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='concepts', to='transactions.Transaction', verbose_name='Transaction')),
            ],
            options={
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ConceptValue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(verbose_name='Amount')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('credit', models.BooleanField(default=True, verbose_name='Credit')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
            ],
            options={
                'verbose_name': 'Concept Value',
                'verbose_name_plural': 'Concept Values',
            },
        ),
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=256, null=True, verbose_name='Name')),
                ('code_a', models.CharField(blank=True, max_length=3, null=True, verbose_name='Alphabetic Code')),
                ('code_n', models.CharField(blank=True, max_length=3, null=True, verbose_name='Numeric Code')),
                ('enabled', models.BooleanField(default=True, verbose_name='Enabled')),
                ('default', models.BooleanField(default=False, verbose_name='Default')),
                ('exchange_rate', models.FloatField(blank=True, null=True, verbose_name='Exchange Rate')),
                ('symbol', models.CharField(blank=True, max_length=3, null=True, verbose_name='Symbol')),
            ],
            options={
                'verbose_name': 'Currency',
                'verbose_name_plural': 'Currencies',
            },
        ),
        migrations.AddField(
            model_name='conceptvalue',
            name='currency',
            field=models.ForeignKey(default=clickgestion.concepts.models.get_default_currency, on_delete=django.db.models.deletion.PROTECT, related_name='values', to='concepts.Currency', verbose_name='Currency'),
        ),
        migrations.AddField(
            model_name='baseconcept',
            name='value',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='concept', to='concepts.ConceptValue', verbose_name='Value'),
        ),
    ]
