#!/usr/bin/env python
import os
import sys
from django.contrib.auth import get_user_model
from clickgestion.transactions.models import Currency
from clickgestion.apt_rentals.models import AptRentalSettings
User = get_user_model()

"""
Create default models
"""


def create_default_models():
    print('Creating default models:')
    create_admin()
    create_dollars()
    create_euros()
    create_pounds()
    create_aptrentalsettings()
    create_nightraterange()
    create_cashfloatdepositsettings()
    create_cashfloatwithdrawalsettings()


def create_test_models():
    create_test_admin()
    create_test_user()


def create_admin():
    with open('/run/secrets/django_admin_user') as f:
        admin_user = f.readline().rstrip('\n')
    try:
        admin = User.objects.get(username=admin_user)
    except:
        with open('/run/secrets/django_admin_email') as f:
            admin_email = f.readline().rstrip('\n')
        with open('/run/secrets/django_admin_pass') as f:
            admin_pass = f.readline().rstrip('\n')
        admin = User.objects.create_superuser(admin_user, admin_email, admin_pass)
    return admin


def create_test_admin():

    user_name = 'admin'
    user_email = 'admin@here.com'
    user_pass = 'admin'
    try:
        admin = User.objects.get(username=user_name)
    except:
        admin = User.objects.create_superuser(user_name, user_email, user_pass)
    return admin


def create_test_user():

    user_name = 'test'
    user_email = 'test@here.com'
    user_pass = 'test'
    try:
        user = User.objects.get(username=user_name)
    except:
        user = User.objects.create_user(user_name, user_email, user_pass)
    return user


def create_euros():
    code_a = 'EUR'
    try:
        currency = Currency.objects.get(code_a=code_a)
    except:
        currency = Currency.objects.create(
            name='Euro',
            code_a=code_a,
            code_n='978',
            default=True,
            exchange_rate=1,
            symbol=u'€',
        )
    return currency


def create_pounds():
    code_a = 'GBP'
    try:
        currency = Currency.objects.get(code_a=code_a)
    except:
        currency = Currency.objects.create(
            name='Pound Sterling',
            code_a=code_a,
            code_n='826',
            exchange_rate=1.2,
            symbol=u'£',
        )
    return currency


def create_dollars():
    code_a = 'USD'
    try:
        currency = Currency.objects.get(code_a=code_a)
    except:
        currency = Currency.objects.create(
            name='US Dollar',
            code_a=code_a,
            code_n='840',
            exchange_rate=0.8,
            symbol=u'$',
        )
    return currency


def create_aptrentalsettings():
    try:
        model = AptRentalSettings.objects.get()
    except:
        model = AptRentalSettings(
            vat_percent=10,
            apt_number_required=False,
            client_address_required=False,
            client_email_required=False,
            client_first_name_required=True,
            client_id_required=True,
            client_last_name_required=True,
            client_phone_number_required=False,
            notes_required=False,
            apt_number_visible=True,
            client_address_visible=True,
            client_email_visible=True,
            client_first_name_visible=True,
            client_id_visible=True,
            client_last_name_visible=True,
            client_phone_number_visible=True,
            notes_visible=True,
        ).save()
    return model


def create_nightraterange():
    from django.utils import timezone
    from clickgestion.apt_rentals.models import NightRateRange
    try:
        model = NightRateRange.objects.get()
    except:
        model = NightRateRange.objects.create(
            start_date=timezone.datetime.today() - timezone.timedelta(days=365),
            end_date=timezone.datetime.today() + timezone.timedelta(days=365),
            monday=10,
            tuesday=20,
            wednesday=30,
            thursday=40,
            friday=50,
            saturday=60,
            sunday=70,
        )
    return model


def create_cashfloatdepositsettings():
    from clickgestion.cash_float.models import CashFloatDepositSettings
    try:
        model = CashFloatDepositSettings.objects.get()
    except:
        model = CashFloatDepositSettings(
            vat_percent=0,
            apt_number_required=False,
            client_address_required=False,
            client_email_required=False,
            client_first_name_required=False,
            client_id_required=False,
            client_last_name_required=False,
            client_phone_number_required=False,
            notes_required=False,
            apt_number_visible=False,
            client_address_visible=False,
            client_email_visible=False,
            client_first_name_visible=False,
            client_id_visible=False,
            client_last_name_visible=False,
            client_phone_number_visible=False,
            notes_visible=True,
        ).save()
    return model


def create_cashfloatwithdrawalsettings():
    from clickgestion.cash_float.models import CashFloatWithdrawalSettings
    try:
        model = CashFloatWithdrawalSettings.objects.get()
    except:
        model = CashFloatWithdrawalSettings(
            vat_percent=0,
            apt_number_required=False,
            client_address_required=False,
            client_email_required=False,
            client_first_name_required=False,
            client_id_required=False,
            client_last_name_required=False,
            client_phone_number_required=False,
            notes_required=False,
            apt_number_visible=False,
            client_address_visible=False,
            client_email_visible=False,
            client_first_name_visible=False,
            client_id_visible=False,
            client_last_name_visible=False,
            client_phone_number_visible=False,
            notes_visible=True,
        ).save()
    return model




