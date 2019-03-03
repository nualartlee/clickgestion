#!/usr/bin/env python
import os
import sys
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from clickgestion.transactions.models import Currency, Transaction
from clickgestion.apt_rentals.models import AptRental, AptRentalDeposit, AptRentalSettings, AptRentalDepositSettings
from clickgestion.apt_rentals.models import NightRateRange
from clickgestion.cash_desk.models import CashFloatDeposit, CashFloatDepositSettings,\
    CashFloatWithdrawal, CashFloatWithdrawalSettings
from django.utils import timezone
from random import randrange
from faker import Faker

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
    for _ in range(100):
        transaction = create_test_open_transaction()
        apt_rental = create_test_apartment_rental(transaction)
        create_test_apartment_rental_deposit(transaction, apt_rental)
        if randrange(2):
            transaction.closed = True
            transaction.closed_date = timezone.datetime.now() - timezone.timedelta(days=randrange(100))
            transaction.save()


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
    try:
        model = NightRateRange.objects.get()
    except:
        model = NightRateRange.objects.create(
            start_date=timezone.now() - timezone.timedelta(days=365),
            end_date=timezone.now() + timezone.timedelta(days=365),
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


def create_test_open_transaction():
    fake = get_faker()
    apt_number = None
    if randrange(100) < 80:
        apt_number = randrange(10, 23) + randrange(10)
    client_address = None
    if randrange(100) < 50:
        client_address = fake.address()
    client_email = None
    if randrange(100) < 40:
        client_email = fake.email()
    client_first_name = None
    if randrange(100) < 90:
        client_first_name = fake.first_name()
    client_id = None
    if randrange(100) < 80:
        client_id = fake.ssn()
    client_last_name = None
    if randrange(100) < 90:
        client_last_name = fake.last_name()
    client_phone_number = None
    if randrange(100) < 30:
        client_phone_number = fake.phone_number()[:14]
    notes = None

    model = Transaction(
        apt_number=apt_number,
        employee=create_test_user(),
        client_address=client_address,
        client_email=client_email,
        client_first_name=client_first_name,
        client_id=client_id,
        client_last_name=client_last_name,
        client_phone_number=client_phone_number,
        notes=notes,
    )
    model.save()
    return model


def create_test_apartment_rental(transaction):
    checkin = timezone.now() + timezone.timedelta(days=randrange(300))
    checkout = checkin + timezone.timedelta(days=randrange(28))
    model = AptRental(
        adults=randrange(1, 5),
        children=randrange(1, 3),
        checkin=checkin,
        checkout=checkout,
        transaction=transaction,
    )
    model.save()
    return model


def create_test_apartment_rental_deposit(transaction, apt_rental):
    model = AptRentalDeposit(
        adults=apt_rental.adults,
        children=apt_rental.children,
        nights=apt_rental.nights,
        transaction=transaction,
    )
    model.save()
    return model


def get_permissions_for_models(models):
    """
    Return a queryset of Permissions given a list of model classes
    :param models: A list of model classes
    :return: Queryset of Permissions
    """
    names = ['Can add {}'.format(model._meta.verbose_name) for model in models]
    return Permission.objects.filter(name__in=names)


def get_faker():
    """
    Get a random localized faker
    :return: Faker()
    """
    selector = randrange(100)
    if 0 <= selector <= 60:
        return Faker('en_GB')
    if 60 < selector <= 75:
        return Faker('es_ES')
    if 75 < selector <= 77:
        return Faker('fr_FR')
    if 77 < selector <= 79:
        return Faker('it_IT')
    if 79 < selector <= 81:
        return Faker('nl_NL')
    if 81 < selector <= 83:
        return Faker('no_NO')
    if 83 < selector <= 85:
        return Faker('de_DE')
    if 85 < selector <= 87:
        return Faker('dk_DK')
    if 87 < selector <= 89:
        return Faker('en_US')
    if 89 < selector <= 91:
        return Faker('en_CA')
    if 91 < selector <= 93:
        return Faker('ru_RU')
    if 93 < selector <= 95:
        return Faker('pt_PT')
    if 95 < selector <= 97:
        return Faker('sv_SE')
    if 97 < selector <= 99:
        return Faker('fi_FI')


