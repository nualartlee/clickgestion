#!/usr/bin/env python
from clickgestion.apt_rentals.models import AptRental, AptRentalSettings
from clickgestion.concepts.models import BaseConcept, ConceptValue, Currency
from clickgestion.cash_desk.models import CashClose, CashFloatDeposit, CashFloatDepositSettings, \
    CashFloatWithdrawal, CashFloatWithdrawalSettings
from decimal import Decimal
from clickgestion.deposits import models as deposit_models
from faker import Faker
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from clickgestion.apt_rentals.models import NightRateRange
from clickgestion.parking_rentals.models import ParkingRental, ParkingRentalSettings
from random import randrange
from clickgestion.refunds.models import Refund, RefundSettings
from clickgestion.safe_rentals.models import SafeRental, SafeRentalSettings
from clickgestion.service_sales.models import Service, ServiceType, ServiceSale, ServiceSaleSettings
from django.conf import settings
from clickgestion.ticket_sales.models import Show, ShowCompany, TicketSale, TicketSaleSettings
from django.utils import timezone
from clickgestion.concepts import totalizers
from clickgestion.transactions.models import Transaction

User = get_user_model()

"""
Create default models
"""


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
            client_signature_required=False,
            department=settings.DEPARTMENTS['production'],
            employee_signature_required=False,
            notes_required=False,
            notes_visible=True,
            vat_percent=10,
            permission_group=Group.objects.get(name=settings.PERMISSION_GROUPS['sales_transaction']),
        ).save()
    return model


def create_aptrentaldepositsettings():
    try:
        model = deposit_models.AptRentalDepositSettings.objects.get()
    except:
        model = deposit_models.AptRentalDepositSettings(
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
            client_signature_required=False,
            department=settings.DEPARTMENTS['deposits'],
            employee_signature_required=False,
            notes_required=False,
            notes_visible=True,
            vat_percent=0,
            permission_group=Group.objects.get(name=settings.PERMISSION_GROUPS['sales_transaction']),
        ).save()
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
            client_signature_required=False,
            department=settings.DEPARTMENTS['cash_desk'],
            employee_signature_required=False,
            notes_required=False,
            notes_visible=True,
            permission_group=Group.objects.get(name=settings.PERMISSION_GROUPS['cash_desk_transaction']),
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
            client_signature_required=False,
            department=settings.DEPARTMENTS['cash_desk'],
            employee_signature_required=False,
            notes_required=False,
            notes_visible=True,
            permission_group=Group.objects.get(name=settings.PERMISSION_GROUPS['cash_desk_transaction']),
            vat_percent=0,
        ).save()
    return model


def create_currency_dollars():
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


def create_currency_euros():
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


def create_currency_pounds():
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


def create_default_models():
    create_admin()
    create_permission_groups()
    create_currency_dollars()
    create_currency_euros()
    create_currency_pounds()
    create_aptrentalsettings()
    create_aptrentaldepositsettings()
    create_nightraterange()
    create_cashfloatdepositsettings()
    create_cashfloatwithdrawalsettings()
    create_depositreturnsettings()
    create_parkingrentalsettings()
    create_parkingrentaldepositsettings()
    create_refundsettings()
    create_saferentalsettings()
    create_saferentaldepositsettings()
    create_shows()
    create_ticketsalesettings()
    create_services()
    create_servicesalesettings()


def create_depositreturnsettings():
    try:
        model = deposit_models.DepositReturnSettings.objects.get()
    except:
        model = deposit_models.DepositReturnSettings(
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
            client_signature_required=True,
            department=settings.DEPARTMENTS['deposits'],
            employee_signature_required=False,
            notes_required=False,
            notes_visible=True,
            permission_group=Group.objects.get(name=settings.PERMISSION_GROUPS['sales_transaction']),
            vat_percent=0,
        ).save()
    return model


def create_group(name, models):
    try:
        group = Group.objects.get(name=name)
    except Group.DoesNotExist:
        group = Group.objects.create(name=name)
        # Add permissions
        for permission in get_permissions_for_models(models):
            if not permission in group.permissions.all():
                group.permissions.add(permission)
        group.save()
    return group


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


def create_parkingrentaldepositsettings():
    try:
        model = deposit_models.ParkingRentalDepositSettings.objects.get()
    except:
        model = deposit_models.ParkingRentalDepositSettings(
            amount=10.0,
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
            client_signature_required=False,
            department=settings.DEPARTMENTS['deposits'],
            employee_signature_required=False,
            notes_required=False,
            notes_visible=True,
            vat_percent=0,
            permission_group=Group.objects.get(name=settings.PERMISSION_GROUPS['sales_transaction']),
        ).save()
    return model


def create_parkingrentalsettings():
    try:
        model = ParkingRentalSettings.objects.get()
    except:
        model = ParkingRentalSettings(
            amount_per_night=5.0,
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
            client_signature_required=False,
            department=settings.DEPARTMENTS['production'],
            employee_signature_required=False,
            notes_required=False,
            notes_visible=True,
            vat_percent=10,
            permission_group=Group.objects.get(name=settings.PERMISSION_GROUPS['sales_transaction']),
        ).save()
    return model


def create_permission_groups():
    sales_models = [
        AptRental,
        deposit_models.AptRentalDeposit,
        deposit_models.DepositReturn,
        ParkingRental,
        deposit_models.ParkingRentalDeposit,
        SafeRental,
        deposit_models.SafeRentalDeposit,
        TicketSale,
        ServiceSale,
    ]
    create_group(settings.PERMISSION_GROUPS['sales_employee'], sales_models)
    sales_models.append(Refund)
    create_group(settings.PERMISSION_GROUPS['sales_transaction'], sales_models)
    cash_models = [CashFloatDeposit, CashFloatWithdrawal]
    create_group(settings.PERMISSION_GROUPS['cash_desk_transaction'], cash_models)
    cash_models.append(CashClose)
    create_group(settings.PERMISSION_GROUPS['cash_desk_employee'], cash_models)


def create_refundsettings():
    try:
        model = RefundSettings.objects.get()
    except:
        model = RefundSettings(
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
            client_signature_required=True,
            department=settings.DEPARTMENTS['production'],
            employee_signature_required=False,
            notes_required=False,
            notes_visible=True,
            permission_group=Group.objects.get(name=settings.PERMISSION_GROUPS['sales_transaction']),
            vat_percent=0,
        ).save()
    return model


def create_saferentaldepositsettings():
    try:
        model = deposit_models.SafeRentalDepositSettings.objects.get()
    except:
        model = deposit_models.SafeRentalDepositSettings(
            amount=10.0,
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
            client_signature_required=False,
            department=settings.DEPARTMENTS['deposits'],
            employee_signature_required=False,
            notes_required=False,
            notes_visible=True,
            vat_percent=0,
            permission_group=Group.objects.get(name=settings.PERMISSION_GROUPS['sales_transaction']),
        ).save()
    return model


def create_saferentalsettings():
    try:
        model = SafeRentalSettings.objects.get()
    except:
        model = SafeRentalSettings(
            amount_per_night=2.0,
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
            client_signature_required=False,
            department=settings.DEPARTMENTS['production'],
            employee_signature_required=False,
            notes_required=False,
            notes_visible=True,
            vat_percent=10,
            permission_group=Group.objects.get(name=settings.PERMISSION_GROUPS['sales_transaction']),
        ).save()
    return model


def create_service(servicetype, name, **kwargs):
    try:
        service = Service.objects.get(name=name)
    except:
        service = Service(servicetype=servicetype, name=name)
        fields = [
            'per_adult',
            'per_child',
            'per_night',
            'per_senior',
            'per_unit',
            'price_per_adult',
            'price_per_child',
            'price_per_senior',
            'price_per_unit',
            'variable_price',
        ]
        for field in fields:
            if kwargs.get(field, False):
                setattr(service, field, kwargs[field])
        service.save()

    return service


def create_services():
    # Room
    servicetype = create_servicetype('Room')
    create_service(servicetype, 'Air Conditioning',
                   per_night=True,
                   per_unit=True, price_per_unit=8,
                   )
    create_service(servicetype, 'Fan',
                   per_night=True,
                   per_unit=True, price_per_unit=4,
                   )
    create_service(servicetype, 'Late Checkout 13:00',
                   price_per_unit=15,
                   date_required=True,
                   )
    create_service(servicetype, 'Late Checkout 14:00',
                   price_per_unit=20,
                   date_required=True,
                   )
    create_service(servicetype, 'Late Checkout 15:00',
                   price_per_unit=30,
                   date_required=True,
                   )
    create_service(servicetype, 'Sheet Change',
                   per_unit=True, price_per_unit=3,
                   date_required=True,
                   )
    create_service(servicetype, 'Towel Change',
                   per_unit=True, price_per_unit=2,
                   date_required=True,
                   )
    # Pool
    servicetype = create_servicetype('Pool')
    create_service(servicetype, 'Pool Float & Towel',
                   per_unit=True, price_per_unit=2,
                   )
    create_service(servicetype, 'Lounger',
                   per_unit=True, price_per_unit=2,
                   )


def create_servicesalesettings():
    try:
        model = ServiceSaleSettings.objects.get()
    except:
        model = ServiceSaleSettings(
            apt_number_required=False,
            apt_number_visible=True,
            client_address_required=False,
            client_address_visible=True,
            client_email_required=False,
            client_email_visible=True,
            client_first_name_required=True,
            client_first_name_visible=True,
            client_id_required=False,
            client_id_visible=True,
            client_last_name_required=True,
            client_last_name_visible=True,
            client_phone_number_required=False,
            client_phone_number_visible=True,
            client_signature_required=False,
            department=settings.DEPARTMENTS['production'],
            employee_signature_required=False,
            notes_required=False,
            notes_visible=True,
            vat_percent=21,
            permission_group=Group.objects.get(name=settings.PERMISSION_GROUPS['sales_transaction']),
        ).save()
    return model


def create_servicetype(name, **kwargs):
    try:
        servicetype = ServiceType.objects.get(name=name)
    except:
        servicetype = ServiceType(name=name)
        servicetype.save()

    return servicetype


def create_show(company, name, **kwargs):
    try:
        show = Show.objects.get(name=name)
    except:
        show = Show(company=company, name=name)
        fields = [
            'per_adult',
            'per_child',
            'per_night',
            'per_senior',
            'per_unit',
            'price_per_adult',
            'price_per_child',
            'price_per_senior',
            'price_per_unit',
            'variable_price',
        ]
        for field in fields:
            if kwargs.get(field, False):
                setattr(show, field, kwargs[field])
        show.save()

    return show


def create_showcompany(name, **kwargs):
    try:
        showcompany = ShowCompany.objects.get(name=name)
    except:
        showcompany = ShowCompany(name=name)
        showcompany.save()

    return showcompany


def create_shows():
    # Amigo24
    showcompany = create_showcompany('Amigo24')
    create_show(showcompany, 'Double Scooter Day',
                per_night=True,
                price_per_unit=20,
                )
    create_show(showcompany, 'Double Scooter Week',
                per_unit=True, price_per_unit=100,
                date_required=True,
                )
    create_show(showcompany, 'Double Scooter Month',
                per_unit=True, price_per_unit=300,
                date_required=True,
                )
    create_show(showcompany, 'Scooter 3 Wheels Day',
                per_night=True,
                price_per_unit=10,
                )
    create_show(showcompany, 'Scooter 3 Wheels Week',
                per_unit=True, price_per_unit=45,
                date_required=True,
                )
    create_show(showcompany, 'Scooter 4 Wheels Day',
                per_night=True,
                price_per_unit=10,
                )
    create_show(showcompany, 'Scooter 4 Wheels Week',
                per_unit=True, price_per_unit=50,
                date_required=True,
                )
    # Aqualandia & Mundomar
    showcompany = create_showcompany('Aqualandia & Mundomar')
    create_show(showcompany, 'Aqualandia Family Ticket 3', per_unit=True, price_per_unit=89.0)
    create_show(showcompany, 'Aqualandia Family Ticket 4', per_unit=True, price_per_unit=112.0)
    create_show(showcompany, 'Aqualandia One Day Ticket',
                per_adult=True, price_per_adult=34.0,
                per_child=True, price_per_child=26.0,
                per_senior=True, price_per_senior=26.0,
                )

    # AquaNatura & TerraNatura
    showcompany = create_showcompany('AquaNatura & TerraNatura')
    create_show(showcompany, 'AquaNatura Large Family Ticket',
                per_adult=True, price_per_adult=20.50,
                per_child=True, price_per_child=17.50,
                per_senior=True, price_per_senior=17.5,
                )
    create_show(showcompany, 'AquaNatura Afternoon Ticket',
                per_adult=True, price_per_adult=24.0,
                per_child=True, price_per_child=19.0,
                per_senior=True, price_per_senior=19.0,
                )
    create_show(showcompany, 'AquaNatura Day Ticket',
                per_adult=True, price_per_adult=32.0,
                per_child=True, price_per_child=26.0,
                per_senior=True, price_per_senior=26.0,
                )
    create_show(showcompany, 'AquaNatura + TerraNatura One Day Ticket',
                per_adult=True, price_per_adult=43.0,
                per_child=True, price_per_child=35.0,
                per_senior=True, price_per_senior=35.0,
                )
    create_show(showcompany, 'AquaNatura + TerraNatura One Day Ticket Large Family',
                per_adult=True, price_per_adult=30.0,
                per_child=True, price_per_child=23.50,
                per_senior=True, price_per_senior=23.50,
                )
    create_show(showcompany, 'AquaNatura + TerraNatura Two Day Ticket',
                per_adult=True, price_per_adult=45.0,
                per_child=True, price_per_child=37.0,
                per_senior=True, price_per_senior=37.0,
                )
    create_show(showcompany, 'AquaNatura + TerraNatura Two Day Ticket Large Family',
                per_adult=True, price_per_adult=31.0,
                per_child=True, price_per_child=25.0,
                per_senior=True, price_per_senior=25.0,
                )
    create_show(showcompany, 'TerraNatura Large Family Ticket',
                per_adult=True, price_per_adult=20.50,
                per_child=True, price_per_child=17.50,
                per_senior=True, price_per_senior=17.5,
                )
    create_show(showcompany, 'TerraNatura Afternoon Ticket',
                per_adult=True, price_per_adult=24.0,
                per_child=True, price_per_child=19.0,
                per_senior=True, price_per_senior=19.0,
                )
    create_show(showcompany, 'TerraNatura Day Ticket',
                per_adult=True, price_per_adult=32.0,
                per_child=True, price_per_child=26.0,
                per_senior=True, price_per_senior=26.0,
                )

    # Benidorm Palace
    showcompany = create_showcompany('Benidorm Palace')
    create_show(showcompany, 'Benidorm Palace Ticket & Drink',
                per_adult=True, price_per_adult=32.0,
                per_child=True, price_per_child=20.0,
                )
    create_show(showcompany, 'Benidorm Palace Ticket & Menu',
                per_adult=True, price_per_adult=52.0,
                per_child=True, price_per_child=25.0,
                )
    create_show(showcompany, 'Benidorm Palace Ticket & Plus Menu',
                per_adult=True, price_per_adult=62.0,
                )
    # Boarding Pass
    showcompany = create_showcompany('Boarding Pass')
    create_show(showcompany, 'Print Service',
                price_per_unit=10,
                variable_price=True,
                )
    # Excursiones Maritimas
    showcompany = create_showcompany('Excursiones Maritimas')
    create_show(showcompany, 'Benidorm Island Return',
                per_adult=True, price_per_adult=15,
                per_child=True, price_per_child=12,
                )
    create_show(showcompany, 'Submarine View (Benidorm Island)',
                per_adult=True, price_per_adult=14,
                per_child=True, price_per_child=11,
                )
    # IMED
    showcompany = create_showcompany('IMED')
    create_show(showcompany, 'Services',
                price_per_unit=100,
                variable_price=True,
                )
    # Karting Benidorm
    showcompany = create_showcompany('Karting Benidorm')
    create_show(showcompany, 'Adult 8 Minutes',
                per_unit=True, price_per_unit=21,
                )
    create_show(showcompany, 'Junior 8 Minutes',
                per_unit=True, price_per_unit=18,
                )
    create_show(showcompany, 'Double 8 Minutes',
                per_unit=True, price_per_unit=22,
                )
    create_show(showcompany, 'Double 8 Minutes',
                per_unit=True, price_per_unit=22,
                )
    create_show(showcompany, 'Fast Race',
                per_unit=True, price_per_unit=35,
                )
    create_show(showcompany, 'Race Experience',
                per_unit=True, price_per_unit=35,
                )
    # Karting Finestrat
    showcompany = create_showcompany('Karting Finestrat')
    create_show(showcompany, 'Mini Prix',
                per_unit=True, price_per_unit=40,
                )
    create_show(showcompany, 'Grand Prix',
                per_unit=True, price_per_unit=50,
                )
    create_show(showcompany, 'Grand Prix + Barbeque',
                per_unit=True, price_per_unit=50,
                )
    create_show(showcompany, 'Super Prix',
                per_unit=True, price_per_unit=60,
                )
    # Localtours
    showcompany = create_showcompany('Localtours')
    create_show(showcompany, 'Guadalest',
                per_adult=True, price_per_adult=33.0,
                per_child=True, price_per_child=16.0,
                )
    create_show(showcompany, 'Costa Blanca Bustour',
                per_adult=True, price_per_adult=49.0,
                per_child=True, price_per_child=25.0,
                )
    create_show(showcompany, 'Costa Blanca Jeep Tour',
                per_adult=True, price_per_adult=59.0,
                per_child=True, price_per_child=30.0,
                )
    create_show(showcompany, 'Costa Blanca Jeep Tour Exclusive 4 Pers.',
                per_unit=True, price_per_adult=225.0,
                )
    create_show(showcompany, 'Jeep Safari Authentic',
                per_adult=True, price_per_adult=65.0,
                per_child=True, price_per_child=35.0,
                )
    create_show(showcompany, 'Jeep Safari Authentic Exclusive 4 Pers.',
                per_unit=True, price_per_unit=225.0,
                )
    create_show(showcompany, 'Viva España Orange Express',
                per_adult=True, price_per_adult=44.0,
                per_child=True, price_per_child=29.0,
                )
    create_show(showcompany, 'FA: Valencia City',
                per_adult=True, price_per_adult=54.0,
                per_child=True, price_per_child=25.0,
                )
    create_show(showcompany, 'FB: Valencia City & Oceanografic',
                per_adult=True, price_per_adult=69.0,
                per_child=True, price_per_child=49.0,
                )
    create_show(showcompany, 'FC: Solo/Only Oceanografic',
                per_adult=True, price_per_adult=64.0,
                per_child=True, price_per_child=43.0,
                )
    create_show(showcompany, 'FD: Valencia Shopping - Por Libre',
                per_adult=True, price_per_adult=45.0,
                per_child=True, price_per_child=20.0,
                )
    create_show(showcompany, 'Discovery Bustour',
                per_adult=True, price_per_adult=59.0,
                per_child=True, price_per_child=33.0,
                )
    create_show(showcompany, 'Alicante Shopping',
                per_adult=True, price_per_adult=39.0,
                per_child=True, price_per_child=20.0,
                )
    create_show(showcompany, 'Costarama / Tabarca Island Incl',
                per_adult=True, price_per_adult=59.0,
                per_child=True, price_per_child=35.0,
                )
    create_show(showcompany, 'Naturama Elche - Alicante',
                per_adult=True, price_per_adult=49.0,
                per_child=True, price_per_child=25.0,
                )
    create_show(showcompany, 'Fallas Valencia',
                per_adult=True, price_per_adult=39.0,
                per_child=True, price_per_child=25.0,
                )
    create_show(showcompany, 'Murcia City',
                per_adult=True, price_per_adult=49.0,
                per_child=True, price_per_child=25.0,
                )
    create_show(showcompany, 'Moros y Cristianos Alcoy Sin Silla',
                per_adult=True, price_per_adult=39.0,
                per_child=True, price_per_child=20.0,
                )
    create_show(showcompany, 'Other',
                per_adult=True, price_per_adult=49.0,
                per_child=True, price_per_child=25.0,
                variable_price=True,
                )
    # Marco Polo
    showcompany = create_showcompany('Marco Polo')
    create_show(showcompany, 'Jeep Safari',
                per_adult=True, price_per_adult=62,
                per_child=True, price_per_child=35,
                )
    create_show(showcompany, 'Jeep Safari Self Drive',
                per_unit=True, price_per_unit=200,
                )
    create_show(showcompany, 'Paintball',
                per_adult=True, price_per_adult=23,
                per_child=True, price_per_child=15,
                )
    create_show(showcompany, 'Paintball + Transport',
                per_unit=True, price_per_unit=30,
                )
    create_show(showcompany, 'Catamaran Sailing Altea',
                per_adult=True, price_per_adult=55,
                per_child=True, price_per_child=33,
                )
    # Profibolta
    showcompany = create_showcompany('Profibolta')
    create_show(showcompany, 'Profibolta Pool', per_unit=True, price_per_unit=2.0)

    # Taxi
    showcompany = create_showcompany('Taxi')
    create_show(showcompany, 'Service',
                variable_price=True, price_per_unit=10.0,
                )


def create_superuser(username, first, last, email):

    try:
        user = User.objects.get(username=username)
    except:
        user = User.objects.create_superuser(
            first_name=first,
            last_name=last,
            username=username,
            email=email,
            password=username,
        )
    return user


def create_test_aptrental(transaction, date, adults=None, children=None, end_date=None, start_date=None):
    if not adults:
        adults = randrange(1, 5)
    if not children:
        children = randrange(5 - adults)
    if not start_date:
        start_date = date + timezone.timedelta(days=randrange(21))
    if not end_date:
        end_date = start_date + timezone.timedelta(days=randrange(1, 28))
    model = AptRental(
        adults=adults,
        children=children,
        start_date=start_date,
        end_date=end_date,
        transaction=transaction,
    )
    model.save()
    AptRental.objects.filter(id=model.id).update(created=date)
    return model


def create_test_aptrentaldeposit(transaction, aptrental, date):
    model = deposit_models.AptRentalDeposit(
        aptrental=aptrental,
        transaction=transaction,
    )
    model.save()
    deposit_models.AptRentalDeposit.objects.filter(id=model.id).update(created=date)
    return model


def create_test_cashclose(date, employee):
    # Withdraw excess balance
    transaction = None

    # Get closed transactions
    closed_transactions = Transaction.objects.filter(closed=True, cashclose=None) \
        .prefetch_related('concepts__value__currency')

    # Get closed concepts
    closed_concepts = BaseConcept.objects.filter(transaction__in=closed_transactions) \
        .prefetch_related('value__currency')

    # Get the balance
    balance = totalizers.get_value_totals(closed_concepts)

    # Withdraw from large amounts
    for dummy_value in balance:
        if dummy_value.amount > 2000:
            withdraw_amount = randrange(int(dummy_value.amount/100)) * 100
            if not transaction:
                transaction = create_test_transaction(employee, date)
            create_test_cashfloatwithdrawal(transaction, date, amount=withdraw_amount, currency=dummy_value.currency)
    if transaction:
        transaction.close(employee)

    fake = Faker()
    notes = None
    if randrange(100) < 30:  # pragma: no cover
        notes = fake.text(max_nb_chars=256)
    elif randrange(100) < 30:  # pragma: no cover
        notes = fake.text(max_nb_chars=128)
    elif randrange(100) < 30:  # pragma: no cover
        notes = fake.text(max_nb_chars=64)
    model = CashClose(
        employee=employee,
        notes=notes,
    )
    model.save()
    CashClose.objects.filter(id=model.id).update(created=date)
    #transactions = Transaction.objects.filter(closed_date__date__lte=date, cashclose=None)
    #if transactions.exists():
    #    for transaction in transactions:
    #        transaction.cashclose = model
    #        transaction.edited = date
    #        transaction.save()
    return model


def create_test_cashfloatdeposit(transaction, date):
    currency = get_random_currency()
    amount = randrange(21) * 100 + randrange(21) * 10 + randrange(21) * 5
    value = ConceptValue(
        currency=currency,
        amount=amount,
    )
    value.save()
    ConceptValue.objects.filter(id=value.id).update(created=date)
    model = CashFloatDeposit(
        value=value,
        transaction=transaction,
    )
    model.save()
    CashFloatDeposit.objects.filter(id=model.id).update(created=date)
    return model


def create_test_cashfloatwithdrawal(transaction, date, currency=None, amount=None):
    if not currency:
        currency = get_random_currency()
    if not amount:
        amount = randrange(21) * 100 + randrange(21) * 10 + randrange(21) * 5
    value = ConceptValue(
        credit=False,
        currency=currency,
        amount=amount,
    )
    value.save()
    ConceptValue.objects.filter(id=value.id).update(created=date)
    model = CashFloatWithdrawal(
        value=value,
        transaction=transaction,
    )
    model.save()
    CashFloatWithdrawal.objects.filter(id=value.id).update(created=date)
    return model


def create_test_client_transaction(employee, date):
    fake = get_faker()
    apt_number = None
    if randrange(100) < 90:  # pragma: no cover
        apt_number = randrange(10, 23)*100 + randrange(10)
    client_address = None
    if randrange(100) < 90:  # pragma: no cover
        client_address = fake.address()
    client_email = None
    if randrange(100) < 90:  # pragma: no cover
        client_email = fake.email()
    client_first_name = None
    if randrange(100) < 90:  # pragma: no cover
        client_first_name = fake.first_name()
    client_id = None
    if randrange(100) < 90:  # pragma: no cover
        client_id = fake.ssn()
    client_last_name = None
    if randrange(100) < 90:  # pragma: no cover
        client_last_name = fake.last_name()
    client_phone_number = None
    if randrange(100) < 90:  # pragma: no cover
        client_phone_number = fake.phone_number()[:14]
    notes = None

    model = Transaction(
        apt_number=apt_number,
        employee=employee,
        client_address=client_address,
        client_email=client_email,
        client_first_name=client_first_name,
        client_id=client_id,
        client_last_name=client_last_name,
        client_phone_number=client_phone_number,
        notes=notes,
    )
    model.code = 'T{}{}'.format(date.strftime('%m%d'), model.code[5:])
    model.save()
    Transaction.objects.filter(code=model.code).update(created=date)
    model.refresh_from_db()
    return model


def create_test_depositreturn(transaction, returned_deposit, date):
    model = deposit_models.DepositReturn(
        returned_deposit=returned_deposit,
        transaction=transaction,
    )
    old_transaction = returned_deposit.transaction
    transaction.client_address = old_transaction.client_address
    transaction.client_first_name = old_transaction.client_first_name
    transaction.client_last_name = old_transaction.client_last_name
    transaction.client_email = old_transaction.client_email
    transaction.client_phone_number = old_transaction.client_phone_number
    transaction.client_id = old_transaction.client_id
    transaction.apt_number = old_transaction.apt_number
    transaction.save()
    model.save()
    deposit_models.DepositReturn.objects.filter(id=model.id).update(created=date)
    return model


def create_test_depositreturns(date):  # pragma: no cover
    deposits_ending_today = BaseConcept.objects.filter(
        end_date__year=date.year,
        end_date__month=date.month,
        end_date__day=date.day,
        concept_class__in=settings.DEPOSIT_CONCEPTS,
    )
    for deposit in deposits_ending_today:
        if deposit.can_return_deposit:
            employee = get_sales_employee()
            transaction = create_test_client_transaction(employee, date)
            create_test_depositreturn(transaction, deposit, date)
            transaction.closed = True
            transaction.closed_date = date
            transaction.save()
            Transaction.objects.filter(id=transaction.id).update(created=date)


def create_test_models(days=30):
    # Do not repeat
    if User.objects.filter(username='dani').exists():  # pragma: no cover
        print('Test models already created')
        return

    create_superuser('dani', 'Daniel', 'Montalba Pee', 'dani@clickgestion.com')
    create_test_users()

    # For each day
    for i in range(days):
        date = timezone.now() - timezone.timedelta(days=days-i)

        # Create random transactions
        for _ in range(randrange(1, 9)):
            create_test_random_transaction(date)

        # Return deposits
        create_test_depositreturns(date)

        # Close Cash Desk
        create_test_cashclose(date, get_cash_employee())

    # Create unaccounted random transactions
    for _ in range(randrange(1, 9)):
        create_test_random_transaction(date)


def create_test_parkingrental(transaction, date, end_date=None, start_date=None):  # pragma: no cover
    if not start_date:
        start_date = date + timezone.timedelta(days=randrange(21))
    if not end_date:
        end_date = start_date + timezone.timedelta(days=randrange(1, 28))
    model = ParkingRental(
        start_date=start_date,
        end_date=end_date,
        transaction=transaction,
    )
    model.save()
    ParkingRental.objects.filter(id=model.id).update(created=date)
    return model


def create_test_parkingrentaldeposit(transaction, parkingrental, date):
    model = deposit_models.ParkingRentalDeposit(
        parkingrental=parkingrental,
        transaction=transaction,
    )
    model.save()
    deposit_models.ParkingRentalDeposit.objects.filter(id=model.id).update(created=date)
    return model


def create_test_random_transaction(date):  # pragma: no cover

    selector = randrange(100)

    # Create client transactions
    if selector <= 92:
        create_test_random_transaction_client(date)

    # Create  house transactions
    if 92 < selector <= 99:
        employee = get_cash_employee()
        transaction = create_test_transaction(employee, date)
        if randrange(100) < 25:
            deposit = create_test_cashfloatdeposit(transaction, date)
        else:
            withdrawal = create_test_cashfloatwithdrawal(transaction, date)

        # Close transaction
        random_close_transaction(transaction)


def create_test_random_transaction_client(date):  # pragma: no cover

    employee = get_sales_employee()
    transaction = create_test_client_transaction(employee, date)
    selector = randrange(100)

    # Apt rental
    if selector <= 40:
        aptrental = create_test_aptrental(transaction, date)
        create_test_aptrentaldeposit(transaction, aptrental, date)

    # Parking rental
    if 40 < selector <= 50:
        parkingrental = create_test_parkingrental(transaction, date)
        create_test_parkingrentaldeposit(transaction, parkingrental, date)

    # Safe rental
    if 50 < selector <= 60:
        saferental = create_test_saferental(transaction, date)
        create_test_saferentaldeposit(transaction, saferental, date)

    # Service sale
    if 60 < selector <= 70:
        servicesale = create_test_servicesale(transaction, date)

    # Ticket sale
    if 70 < selector <= 80:
        ticketsale = create_test_ticketsale(transaction, date)

    # Deposit return
    if 80 < selector <= 95:
        apt_rental_deposits = deposit_models.AptRentalDeposit.objects.filter(
            transaction__closed=True, depositreturns=None).reverse()
        if not apt_rental_deposits:
            return None
        apt_rental_deposit = apt_rental_deposits[0]
        create_test_depositreturn(transaction, apt_rental_deposit, date)

    # Refund
    if 96 < selector <= 99:
        concepts = BaseConcept.objects.all()
        for concept in concepts:
            if concept.can_refund:
                refunded_concept = concept
                create_test_refund(transaction, refunded_concept, date)
                break

    # Close transaction
    random_close_transaction(transaction)


def create_test_refund(transaction, refunded_concept, date):
    model = Refund(
        refunded_concept=refunded_concept,
        transaction=transaction,
    )
    model.save()
    deposit_models.DepositReturn.objects.filter(id=model.id).update(created=date)
    return model


def create_test_saferental(transaction, date, end_date=None, start_date=None):  # pragma: no cover
    if not start_date:
        start_date = date + timezone.timedelta(days=randrange(21))
    if not end_date:
        end_date = start_date + timezone.timedelta(days=randrange(1, 28))
    model = SafeRental(
        start_date=start_date,
        end_date=end_date,
        transaction=transaction,
    )
    model.save()
    SafeRental.objects.filter(id=model.id).update(created=date)
    return model


def create_test_saferentaldeposit(transaction, saferental, date):
    model = deposit_models.SafeRentalDeposit(
        saferental=saferental,
        transaction=transaction,
    )
    model.save()
    deposit_models.SafeRentalDeposit.objects.filter(id=model.id).update(created=date)
    return model


def create_test_servicesale(
        transaction, date, service=None, start_date=None, end_date=None,
        adults=None, children=None, seniors=None, units=None):  # pragma: no cover
    if not service:
        services = Service.objects.all()
        selector = randrange(services.count())
        service = services[selector]
    kwargs = {
        'service': service,
        'transaction': transaction,
        'per_adult': service.per_adult,
        'per_child': service.per_child,
        'per_night': service.per_night,
        'per_senior': service.per_senior,
        'per_unit': service.per_unit,
    }
    if service.date_required or service.per_night:
        if not start_date:
            start_date = date + timezone.timedelta(days=randrange(21))
        kwargs['start_date'] = start_date
    if service.per_night:
        if not end_date:
            end_date = start_date + timezone.timedelta(days=randrange(1, 28))
        kwargs['end_date'] = end_date
    if service.per_adult:
        if not adults:
            adults = randrange(1, 5)
        kwargs['adults'] = adults
        if service.variable_price:
            kwargs['price_per_adult'] = Decimal(randrange(20, 100) / 2)
        else:
            kwargs['price_per_adult'] = service.price_per_adult
    if service.per_child:
        if not children:
            children = randrange(1, 5)
        kwargs['children'] = children
        if service.variable_price:
            kwargs['price_per_child'] = Decimal(randrange(20, 80) / 2)
        else:
            kwargs['price_per_child'] = service.price_per_child
    if service.per_senior:
        if not seniors:
            seniors = randrange(1, 5)
        kwargs['seniors'] = seniors
        if service.variable_price:
            kwargs['price_per_senior'] = Decimal(randrange(20, 90) / 2)
        else:
            kwargs['price_per_senior'] = service.price_per_senior
    if service.per_unit:
        if not units:
            units = randrange(1, 5)
        kwargs['units'] = units
    if service.variable_price:
        kwargs['price_per_unit'] = Decimal(randrange(20, 200) / 2)
    else:
        kwargs['price_per_unit'] = service.price_per_unit
    model = ServiceSale(**kwargs)
    model.save()
    ServiceSale.objects.filter(id=model.id).update(created=date)
    model.refresh_from_db()
    return model


def create_test_ticketsale(
        transaction, date, show=None, start_date=None, end_date=None,
        adults=None, children=None, seniors=None, units=None):  # pragma: no cover
    if not show:
        shows = Show.objects.all()
        selector = randrange(shows.count())
        show = shows[selector]
    kwargs = {
        'show': show,
        'transaction': transaction,
        'per_adult': show.per_adult,
        'per_child': show.per_child,
        'per_night': show.per_night,
        'per_senior': show.per_senior,
        'per_unit': show.per_unit,
    }
    if show.date_required or show.per_night:
        if not start_date:
            start_date = date + timezone.timedelta(days=randrange(21))
        kwargs['start_date'] = start_date
    if show.per_night:
        if not end_date:
            end_date = start_date + timezone.timedelta(days=randrange(1, 28))
        kwargs['end_date'] = end_date
    if show.per_adult:
        if not adults:
            adults = randrange(1, 5)
        kwargs['adults'] = adults
        if show.variable_price:
            kwargs['price_per_adult'] = Decimal(randrange(20, 100) / 2)
        else:
            kwargs['price_per_adult'] = show.price_per_adult
    if show.per_child:
        if not children:
            children = randrange(1, 5)
        kwargs['children'] = children
        if show.variable_price:
            kwargs['price_per_child'] = Decimal(randrange(20, 80) / 2)
        else:
            kwargs['price_per_child'] = show.price_per_child
    if show.per_senior:
        if not seniors:
            seniors = randrange(1, 5)
        kwargs['seniors'] = seniors
        if show.variable_price:
            kwargs['price_per_senior'] = Decimal(randrange(20, 90) / 2)
        else:
            kwargs['price_per_senior'] = show.price_per_senior
    if show.per_unit:
        if not units:
            units = randrange(1, 5)
        kwargs['units'] = units
    if show.variable_price:
        kwargs['price_per_unit'] = Decimal(randrange(20, 200) / 2)
    else:
        kwargs['price_per_unit'] = show.price_per_unit
    model = TicketSale(**kwargs)
    model.save()
    TicketSale.objects.filter(id=model.id).update(created=date)
    model.refresh_from_db()
    return model


def create_test_transaction(employee, date):
    fake = Faker()
    notes = None
    if randrange(100) < 40:  # pragma: no cover
        notes = fake.text()

    model = Transaction(
        employee=employee,
        notes=notes,
    )
    model.code = 'T{}{}'.format(date.strftime('%m%d'), model.code[5:])
    model.save()
    Transaction.objects.filter(id=model.id).update(created=date)
    model.refresh_from_db()
    return model


def create_test_users():
    sgroup = create_group('Sales Employees', [])
    cgroup = create_group('Cash Employees', [])
    create_user('sebas', 'Sebastian', 'Panti', 'sebas@clickgestion.com', [sgroup, cgroup])
    create_user('manu', 'Manuel', 'Borges', 'manu@clickgestion.com', [sgroup, cgroup])
    create_user('vanesa', 'Vanesa', 'Perez Del Mar', 'vanesa@clickgestion.com', [sgroup, cgroup])
    create_user('isidro', 'Isidro', 'Del Rey Rodriguez', 'isidro@clickgestion.com', [sgroup])
    create_user('juan', 'Juan Carlos', 'Muni', 'juan@clickgestion.com', [sgroup])
    create_user('angel', 'Angel', 'Morales Parda', 'angel@clickgestion.com', [sgroup])
    create_user('toni', 'Toni', 'Vera Miralles', 'toni@clickgestion.com', [sgroup])
    create_user('natalia', 'Natalia', 'Villa Martinez', 'natalia@clickgestion.com', [sgroup, cgroup])
    create_user('marcos', 'Marcos', 'Ruiz Pantaloni', 'marcos@clickgestion.com', [sgroup, cgroup])
    create_user('suzi', 'Suzan', 'Williams', 'suzi@clickgestion.com', [sgroup, cgroup])


def create_ticketsalesettings():
    try:
        model = TicketSaleSettings.objects.get()
    except:
        model = TicketSaleSettings(
            apt_number_required=False,
            apt_number_visible=True,
            client_address_required=False,
            client_address_visible=True,
            client_email_required=False,
            client_email_visible=True,
            client_first_name_required=True,
            client_first_name_visible=True,
            client_id_required=False,
            client_id_visible=True,
            client_last_name_required=True,
            client_last_name_visible=True,
            client_phone_number_required=False,
            client_phone_number_visible=True,
            client_signature_required=False,
            department=settings.DEPARTMENTS['production'],
            employee_signature_required=False,
            notes_required=False,
            notes_visible=True,
            vat_percent=21,
            permission_group=Group.objects.get(name=settings.PERMISSION_GROUPS['sales_transaction']),
        ).save()
    return model


def create_user(username, first, last, email, groups):

    try:
        user = User.objects.get(username=username)
    except:
        user = User.objects.create_user(
            first_name=first,
            last_name=last,
            username=username,
            email=email,
            password=username,
        )
        for group in groups:
            user.groups.add(group)
        user.save()
    return user


def get_cash_employee():
    group = create_group('Cash Employees', [])
    users = group.user_set.all()
    return users[randrange(users.count())]


def get_faker():  # pragma: no cover
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


def get_sales_employee():
    group = create_group('Sales Employees', [])
    users = group.user_set.all()
    return users[randrange(users.count())]


def get_permissions_for_models(models):
    """
    Return a queryset of Permissions given a list of model classes
    :param models: A list of model classes
    :return: Queryset of Permissions
    """
    names = ['Can add {}'.format(model._meta.verbose_name) for model in models]
    return Permission.objects.filter(name__in=names)


def get_random_currency():
    currencies = Currency.objects.all()
    selector = randrange(100)
    if 0 <= selector <= 90:  # pragma: no cover
        return Currency.objects.get(code_a='EUR')
    if 90 < selector <= 98:  # pragma: no cover
        return Currency.objects.get(code_a='GBP')
    if 98 < selector <= 99:  # pragma: no cover
        return Currency.objects.get(code_a='USD')
    return Currency.objects.get(code_a='EUR')  # pragma: no cover


def random_close_transaction(transaction):
    """
    Randomly choose if a transaction is closed
    """

    days_elapsed = (timezone.now() - transaction.created).days
    closed_chance = 0.5 * days_elapsed + 85
    selector = randrange(100)
    if selector < closed_chance:
        transaction.closed = True
        transaction.closed_date = transaction.created
        transaction.save()


