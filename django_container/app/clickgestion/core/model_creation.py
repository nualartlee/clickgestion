#!/usr/bin/env python
import os
import sys
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from clickgestion.concepts.models import BaseConcept, ConceptValue, Currency
from clickgestion.deposits import models as deposit_models
from clickgestion.transactions.models import Transaction
from clickgestion.apt_rentals.models import AptRental, AptRentalSettings
from clickgestion.apt_rentals.models import NightRateRange
from clickgestion.cash_desk.models import CashClose, CashFloatDeposit, CashFloatDepositSettings,\
    CashFloatWithdrawal, CashFloatWithdrawalSettings
from clickgestion.parking_rentals.models import ParkingRental, ParkingRentalSettings
from clickgestion.refunds.models import Refund, RefundSettings
from django.utils import timezone
from random import randrange
from faker import Faker

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
            accounting_group='Production',
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
            employee_signature_required=False,
            notes_required=False,
            notes_visible=True,
            vat_percent=10,
            permission_group=Group.objects.get(name='Sales Transaction'),
        ).save()
    return model


def create_aptrentaldepositsettings():
    try:
        model = deposit_models.AptRentalDepositSettings.objects.get()
    except:
        model = deposit_models.AptRentalDepositSettings(
            accounting_group='Deposits',
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
            employee_signature_required=False,
            notes_required=False,
            notes_visible=True,
            vat_percent=0,
            permission_group=Group.objects.get(name='Sales Transaction'),
        ).save()
    return model


def create_cashfloatdepositsettings():
    try:
        model = CashFloatDepositSettings.objects.get()
    except:
        model = CashFloatDepositSettings(
            accounting_group='Cash',
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
            employee_signature_required=False,
            notes_required=False,
            notes_visible=True,
            permission_group=Group.objects.get(name='Cash Transaction'),
            vat_percent=0,
        ).save()
    return model


def create_cashfloatwithdrawalsettings():
    try:
        model = CashFloatWithdrawalSettings.objects.get()
    except:
        model = CashFloatWithdrawalSettings(
            accounting_group='Cash',
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
            employee_signature_required=False,
            notes_required=False,
            notes_visible=True,
            permission_group=Group.objects.get(name='Cash Transaction'),
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


def create_depositreturnsettings():
    try:
        model = deposit_models.DepositReturnSettings.objects.get()
    except:
        model = deposit_models.DepositReturnSettings(
            accounting_group='Deposits',
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
            employee_signature_required=False,
            notes_required=False,
            notes_visible=True,
            permission_group=Group.objects.get(name='Sales Transaction'),
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
            accounting_group='Deposits',
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
            employee_signature_required=False,
            notes_required=False,
            notes_visible=True,
            vat_percent=0,
            permission_group=Group.objects.get(name='Sales Transaction'),
        ).save()
    return model


def create_parkingrentalsettings():
    try:
        model = ParkingRentalSettings.objects.get()
    except:
        model = ParkingRentalSettings(
            amount_per_night=5.0,
            accounting_group='Production',
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
            employee_signature_required=False,
            notes_required=False,
            notes_visible=True,
            vat_percent=10,
            permission_group=Group.objects.get(name='Sales Transaction'),
        ).save()
    return model


def create_permission_groups():
    models = [CashFloatDeposit, CashFloatWithdrawal]
    create_group('Cash Employees', models)
    models = [AptRental, deposit_models.AptRentalDeposit, ParkingRental, deposit_models.DepositReturn]
    create_group('Sales Employees', models)
    models = [AptRental, deposit_models.AptRentalDeposit, ParkingRental, deposit_models.DepositReturn, Refund]
    create_group('Sales Transaction', models)
    models = [CashFloatDeposit, CashFloatWithdrawal]
    create_group('Cash Transaction', models)


def create_refundsettings():
    try:
        model = RefundSettings.objects.get()
    except:
        model = RefundSettings(
            accounting_group='Sales',
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
            employee_signature_required=False,
            notes_required=False,
            notes_visible=True,
            permission_group=Group.objects.get(name='Sales Transaction'),
            vat_percent=0,
        ).save()
    return model


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
    transactions = Transaction.objects.filter(closed_date__date__lte=date, cashclose=None)
    if transactions.exists():
        for transaction in transactions:
            transaction.cashclose = model
            transaction.edited = date
            transaction.save()
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


def create_test_cashfloatwithdrawal(transaction, date):
    currency = get_random_currency()
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
    apt_rental_deposits_ending_today = deposit_models.AptRentalDeposit.objects.filter(
        end_date__year=date.year,
        end_date__month=date.month,
        end_date__day=date.day,
    )
    for deposit in apt_rental_deposits_ending_today:
        if not deposit.transaction.closed:
            continue
        if deposit.deposit_return:
            continue
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
    if selector <= 70:
        aptrental = create_test_aptrental(transaction, date)
        create_test_aptrentaldeposit(transaction, aptrental, date)

    # Parking rental
    if 70 < selector <= 80:
        parkingrental = create_test_parkingrental(transaction, date)
        create_test_parkingrentaldeposit(transaction, parkingrental, date)

    # Deposit return
    if 80 < selector <= 95:
        apt_rental_deposits = deposit_models.AptRentalDeposit.objects.filter(transaction__closed=True, depositreturns=None).reverse()
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


