#!/usr/bin/env python
import os
import sys

"""
Create default models
"""


def create_default_models():
    # Create default users
    print('\n')
    print('Creating default users:')
    from django.contrib.auth import get_user_model
    User = get_user_model()

    # Create real admin
    with open('/run/secrets/django_admin_user') as f:
        admin_user = f.readline().rstrip('\n')
    try:
        User.objects.get(username=admin_user)
        print("Admin user already exists")
    except:
        with open('/run/secrets/django_admin_email') as f:
            admin_email = f.readline().rstrip('\n')
        with open('/run/secrets/django_admin_pass') as f:
            admin_pass = f.readline().rstrip('\n')
        User.objects.create_superuser(admin_user, admin_email, admin_pass)
        print("Admin user created")
        print("{0} ({1})\n{2}".format(admin_user, admin_email, admin_pass))

    # Create test users
    print('\n')
    print('Creating test users:')

    # Create test admin
    user_name = 'admin'
    user_email = 'admin@here.com'
    user_pass = 'admin'
    try:
        User.objects.get(username=user_name)
        print("{} testuser already exists".format(user_name))
    except:
        User.objects.create_superuser(user_name, user_email, user_pass)
        print("{} testuser created".format(user_name))

    # Create test user
    user_name = 'test'
    user_email = 'test@here.com'
    user_pass = 'test'
    try:
        User.objects.get(username=user_name)
        print("{} testuser already exists".format(user_name))
    except:
        User.objects.create_user(user_name, user_email, user_pass)
        print("{} testuser created".format(user_name))

    # Create currencies
    print('\n')
    print("Creating currencies")
    from clickgestion.transactions.models import Currency
    # EUR
    code_a = 'EUR'
    try:
        Currency.objects.get(code_a=code_a)
        print('{} currency already exists'.format(code_a))
    except:
        Currency.objects.create(
            name='Euro',
            code_a=code_a,
            code_n='978',
            default=True,
            exchange_rate=1,
            symbol=u'€',
        )
        print('{} currency created'.format(code_a))
    # GBP
    code_a = 'GBP'
    try:
        Currency.objects.get(code_a=code_a)
        print('{} currency already exists'.format(code_a))
    except:
        Currency.objects.create(
            name='Pound Sterling',
            code_a=code_a,
            code_n='826',
            exchange_rate=1.2,
            symbol=u'£',
        )
        print('{} currency created'.format(code_a))
    # USD
    code_a = 'USD'
    try:
        Currency.objects.get(code_a=code_a)
        print('{} currency already exists'.format(code_a))
    except:
        Currency.objects.create(
            name='US Dollar',
            code_a=code_a,
            code_n='840',
            exchange_rate=0.8,
            symbol=u'$',
        )
        print('{} currency created'.format(code_a))

    # Creating AptRentalSettings
    print('\n')
    print("Creating AptRentalSettings")
    from clickgestion.apt_rentals.models import AptRentalSettings
    try:
        AptRentalSettings.objects.get()
        print('AptRentalSettings already exists')
    except:
        AptRentalSettings(
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
        print('AptRentalSettings created')

    # Create NightRateRange
    print('\n')
    print("Creating NightRateRange")
    from django.utils import timezone
    from clickgestion.apt_rentals.models import NightRateRange
    try:
        NightRateRange.objects.get()
        print('NightRateRange already exists')
    except:
        NightRateRange.objects.create(
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
        print("NightRateRange created")

    # Creating CashFloatDepositSettings
    print('\n')
    print("Creating CashFloatDepositSettings")
    from clickgestion.cash_float.models import CashFloatDepositSettings
    try:
        CashFloatDepositSettings.objects.get()
        print('CashFloatDepositSettings already exists')
    except:
        CashFloatDepositSettings(
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
        print('CashFloatDepositSettings created')

    # Creating CashFloatWithdrawalSettings
    print('\n')
    print("Creating CashFloatWithdrawalSettings")
    from clickgestion.cash_float.models import CashFloatWithdrawalSettings
    try:
        CashFloatWithdrawalSettings.objects.get()
        print('CashFloatWithdrawalSettings already exists')
    except:
        CashFloatWithdrawalSettings(
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
        print('CashFloatWithdrawalSettings created')
