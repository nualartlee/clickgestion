# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2019-03-28 21:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
        ('concepts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('baseconcept_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='concepts.BaseConcept')),
                ('refunded_concept', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='refunds', to='concepts.BaseConcept', verbose_name='Refunded Concept')),
            ],
            options={
                'verbose_name': 'Refund',
                'verbose_name_plural': 'Refunds',
            },
            bases=('concepts.baseconcept',),
        ),
        migrations.CreateModel(
            name='RefundSettings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accounting_group', models.CharField(blank=True, max_length=32, null=True, verbose_name='Accounting Group')),
                ('apt_number_required', models.BooleanField(default=False, verbose_name='Apt Number Required')),
                ('apt_number_visible', models.BooleanField(default=True, verbose_name='Apt Number Visible')),
                ('client_address_required', models.BooleanField(default=False, verbose_name='Address Required')),
                ('client_address_visible', models.BooleanField(default=True, verbose_name='Address Visible')),
                ('client_email_required', models.BooleanField(default=False, verbose_name='Email Required')),
                ('client_email_visible', models.BooleanField(default=True, verbose_name='Email Visible')),
                ('client_first_name_required', models.BooleanField(default=False, verbose_name='First Name Required')),
                ('client_first_name_visible', models.BooleanField(default=True, verbose_name='First Name Visible')),
                ('client_id_required', models.BooleanField(default=False, verbose_name='Passport/ID Required')),
                ('client_id_visible', models.BooleanField(default=True, verbose_name='Passport/ID Visible')),
                ('client_last_name_required', models.BooleanField(default=False, verbose_name='Last Name Required')),
                ('client_last_name_visible', models.BooleanField(default=True, verbose_name='Last Name Visible')),
                ('client_phone_number_required', models.BooleanField(default=False, verbose_name='Phone Required')),
                ('client_phone_number_visible', models.BooleanField(default=True, verbose_name='Phone Visible')),
                ('client_signature_required', models.BooleanField(default=False, verbose_name='Client Signature Required')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Created')),
                ('employee_signature_required', models.BooleanField(default=False, verbose_name='Employee Signature Required')),
                ('notes_required', models.BooleanField(default=False, verbose_name='Notes Required')),
                ('notes_visible', models.BooleanField(default=True, verbose_name='Notes Visible')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Updated')),
                ('vat_percent', models.FloatField(default=0, verbose_name='VAT Percent')),
                ('permission_group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.Group', verbose_name='Permission Group')),
            ],
            options={
                'verbose_name': 'Refund Settings',
                'verbose_name_plural': 'Refund Settings',
            },
        ),
    ]
