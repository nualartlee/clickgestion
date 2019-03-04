#!/usr/bin/env python
import os
import sys
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from clickgestion.transactions.models import ConceptValue, Currency, Transaction
from clickgestion.apt_rentals.models import AptRental, AptRentalDeposit, AptRentalSettings, AptRentalDepositSettings
from clickgestion.apt_rentals.models import NightRateRange
from clickgestion.cash_desk.models import CashClose, CashFloatDeposit, CashFloatDepositSettings,\
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


def create_test_models(days=30):
    create_superuser('dani', 'Daniel', 'Montalba Pee', 'dani@clickgestion.com')
    create_test_users()

    # For each day
    for i in range(days):
        date = timezone.now() - timezone.timedelta(days=days-i)

        # Create random transactions
        for _ in range(randrange(1, 9)):
            create_test_random_transaction(date)

        # Close Cash Desk
        create_test_cashclose(date, get_cash_employee())

    # Create unaccounted random transactions
    for _ in range(randrange(1, 9)):
        create_test_random_transaction(date)


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
            vat_percent=0,
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


def create_test_transaction(employee, date):
    fake = Faker()
    notes = None
    if randrange(100) < 40:
        notes = fake.text()

    model = Transaction(
        created=date,
        employee=employee,
        notes=notes,
    )
    model.code = 'T{}{}'.format(date.strftime('%m%d'), model.code[5:])
    model.save()
    return model


def create_test_client_transaction(employee, date):
    fake = get_faker()
    apt_number = None
    if randrange(100) < 90:
        apt_number = randrange(10, 23)*100 + randrange(10)
    client_address = None
    if randrange(100) < 90:
        client_address = fake.address()
    client_email = None
    if randrange(100) < 90:
        client_email = fake.email()
    client_first_name = None
    if randrange(100) < 90:
        client_first_name = fake.first_name()
    client_id = None
    if randrange(100) < 90:
        client_id = fake.ssn()
    client_last_name = None
    if randrange(100) < 90:
        client_last_name = fake.last_name()
    client_phone_number = None
    if randrange(100) < 90:
        client_phone_number = fake.phone_number()[:14]
    notes = None

    model = Transaction(
        apt_number=apt_number,
        employee=employee,
        created=date,
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
    return model


def create_test_apartment_rental(transaction, date):
    checkin = date + timezone.timedelta(days=randrange(21))
    checkout = checkin + timezone.timedelta(days=randrange(28))
    model = AptRental(
        adults=randrange(1, 5),
        children=randrange(1, 3),
        checkin=checkin,
        checkout=checkout,
        transaction=transaction,
        created=date,
    )
    model.save()
    return model


def create_test_apartment_rental_deposit(transaction, apt_rental, date):
    model = AptRentalDeposit(
        adults=apt_rental.adults,
        children=apt_rental.children,
        nights=apt_rental.nights,
        transaction=transaction,
        created=date,
    )
    model.save()
    return model


def create_test_cashclose(date, employee):
    fake = Faker()
    notes = None
    if randrange(100) < 60:
        notes = fake.text(max_nb_chars=512)
    model = CashClose(
        created=date,
        employee=employee,
        notes=notes,
    )
    model.save()
    transactions = Transaction.objects.filter(closed_date__date__lte=date, cashclose=None)
    if transactions.exists():
        for transaction in transactions:
            transaction.cashclose = model
            transaction.edited = date
            transaction.save()
    return model


def create_test_cash_float_deposit(transaction, date):
    currency = get_random_currency()
    amount = randrange(21) * 100 + randrange(21) * 10 + randrange(21) * 5
    value = ConceptValue(
        currency=currency,
        amount=amount,
        created=date,
    )
    value.save()
    model = CashFloatDeposit(
        value=value,
        transaction=transaction,
        created=date,
    )
    model.save()
    return model


def create_test_cash_float_withdrawal(transaction, date):
    currency = get_random_currency()
    amount = randrange(21) * 100 + randrange(21) * 10 + randrange(21) * 5
    value = ConceptValue(
        currency=currency,
        amount=amount,
        created=date,
    )
    value.save()
    model = CashFloatWithdrawal(
        value=value,
        transaction=transaction,
        created=date,
    )
    model.save()
    return model


def create_test_random_transaction(date):

    selector = randrange(100)

    # Create closed client transactions
    if selector <= 80:
        employee = get_sales_employee()
        transaction = create_test_client_transaction(employee, date)
        apt_rental = create_test_apartment_rental(transaction, date)
        create_test_apartment_rental_deposit(transaction, apt_rental, date)
        transaction.closed = True
        transaction.closed_date = date
        transaction.save()

    # Create closed house transactions
    if 80 < selector <= 92:
        employee = get_cash_employee()
        transaction = create_test_transaction(employee, date)
        if randrange(100) < 25:
            deposit = create_test_cash_float_deposit(transaction, date)
        else:
            withdrawal = create_test_cash_float_withdrawal(transaction, date)
        transaction.closed = True
        transaction.closed_date = date
        transaction.save()

    # Create open client transactions
    if 92 < selector <= 98:
        employee = get_sales_employee()
        transaction = create_test_client_transaction(employee, date)
        apt_rental = create_test_apartment_rental(transaction, date)
        create_test_apartment_rental_deposit(transaction, apt_rental, date)

    # Create open house transactions
    if 98 < selector <= 99:
        employee = get_cash_employee()
        transaction = create_test_transaction(employee, date)
        if randrange(100) < 25:
            deposit = create_test_cash_float_deposit(transaction, date)
        else:
            withdrawal = create_test_cash_float_withdrawal(transaction, date)

    return transaction


def create_test_users():
    sgroup = create_sales_group()
    cgroup = create_cash_group()
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


def get_cash_employee():
    group = create_cash_group()
    users = group.user_set.all()
    return users[randrange(users.count())]


def get_sales_employee():
    group = create_sales_group()
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


def get_random_currency():
    selector = randrange(100)
    if 0 <= selector <= 90:
        return Currency.objects.get(code_a='EUR')
    if 90 < selector <= 98:
        return Currency.objects.get(code_a='GBP')
    if 98 < selector <= 99:
        return Currency.objects.get(code_a='USD')
    return Currency.objects.get(code_a='EUR')

