#!/usr/bin/env python
import os
import sys
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from clickgestion.transactions.models import Currency
from clickgestion.apt_rentals.models import AptRental, AptRentalDeposit, AptRentalSettings, AptRentalDepositSettings
from clickgestion.cash_desk.models import CashFloatDeposit, CashFloatWithdrawal
User = get_user_model()

"""
Create default models
"""


def create_default_models():
    create_admin()
    create_sales_group()
    create_cash_group()
    create_dollars()
    create_euros()
    create_pounds()
    create_aptrentalsettings()
    create_aptrentaldepositsettings()
    create_nightraterange()
    create_cashfloatdepositsettings()
    create_cashfloatwithdrawalsettings()


def create_test_models():
    create_test_admin()
    create_test_user()


def create_group(name, permissions):
    try:
        group = Group.objects.get(name=name)
    except Group.DoesNotExist:
        group = Group.objects.create(name=name)
        # Add permissions
        for permission in get_permissions_for_models([CashFloatDeposit, CashFloatWithdrawal]):
            if not permission in group.permissions.all():
                group.permissions.add(permission)
        group.save()
    return group


def create_cash_group():
    return create_group('cash', [CashFloatDeposit, CashFloatWithdrawal])


def create_sales_group():
    return create_group('sales', [AptRental, AptRentalDeposit])


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
            apt_number_required=False,
            apt_number_visible=True,
            client_address_required=False,
            client_address_visible=True,
            client_email_required=False,
            client_email_visible=True,
            client_first_name_required=True,
            client_first_name_visible=True,
            client_id_required=True,
            client_id_visible=True,
            client_last_name_required=True,
            client_last_name_visible=True,
            client_phone_number_required=False,
            client_phone_number_visible=True,
            notes_required=False,
            notes_visible=True,
            vat_percent=10,
            permission_group=Group.objects.get(name='sales'),
        ).save()
    return model


def create_aptrentaldepositsettings():
    try:
        model = AptRentalDepositSettings.objects.get()
    except:
        model = AptRentalDepositSettings(
            apt_number_required=False,
            apt_number_visible=True,
            client_address_required=False,
            client_address_visible=True,
            client_email_required=False,
            client_email_visible=True,
            client_first_name_required=True,
            client_first_name_visible=True,
            client_id_required=True,
            client_id_visible=True,
            client_last_name_required=True,
            client_last_name_visible=True,
            client_phone_number_required=False,
            client_phone_number_visible=True,
            notes_required=False,
            notes_visible=True,
            vat_percent=10,
            permission_group=Group.objects.get(name='sales'),
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
    from clickgestion.cash_desk.models import CashFloatDepositSettings
    try:
        model = CashFloatDepositSettings.objects.get()
    except:
        model = CashFloatDepositSettings(
            apt_number_required=False,
            apt_number_visible=False,
            client_address_required=False,
            client_address_visible=False,
            client_email_required=False,
            client_email_visible=False,
            client_first_name_required=False,
            client_first_name_visible=False,
            client_id_required=False,
            client_id_visible=False,
            client_last_name_required=False,
            client_last_name_visible=False,
            client_phone_number_required=False,
            client_phone_number_visible=False,
            notes_required=False,
            notes_visible=True,
            permission_group=Group.objects.get(name='cash'),
            vat_percent=0,
        ).save()
    return model


def create_cashfloatwithdrawalsettings():
    from clickgestion.cash_desk.models import CashFloatWithdrawalSettings
    try:
        model = CashFloatWithdrawalSettings.objects.get()
    except:
        model = CashFloatWithdrawalSettings(
            apt_number_required=False,
            apt_number_visible=False,
            client_address_required=False,
            client_address_visible=False,
            client_email_required=False,
            client_email_visible=False,
            client_first_name_required=False,
            client_first_name_visible=False,
            client_id_required=False,
            client_id_visible=False,
            client_last_name_required=False,
            client_last_name_visible=False,
            client_phone_number_required=False,
            client_phone_number_visible=False,
            notes_required=False,
            notes_visible=True,
            permission_group=Group.objects.get(name='cash'),
            vat_percent=0,
        ).save()
    return model


def get_permissions_for_models(models):
    """
    Return a queryset of Permissions given a list of model classes
    :param models: A list of model classes
    :return: Queryset of Permissions
    """
    names = ['Can add {}'.format(model._meta.verbose_name) for model in models]
    return Permission.objects.filter(name__in=names)




