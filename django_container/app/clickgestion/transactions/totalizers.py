from django.apps import apps
from django.conf import settings
from django.utils.translation import gettext_lazy


class BreakdownType:
    def __init__(self, type, values, concept_count, totals):
        self.values = values
        self.concept_count = concept_count
        self.totals = totals
        self.type = type


class DummyValue:
    def __init__(self, amount, credit, currency):
        self.amount = amount
        self.credit = credit
        self.currency = currency


def get_breakdown_by_accounting_group(transaction_set):
    """

    :param transaction_set: A set of transactions
    :return: A list of objects with the breakdown
    """
    pass


def get_breakdown_by_concept_type(transaction_set):
    """

    :param transaction_set: A set of transactions
    :return: A list of objects with the breakdown
    """

    # Get breakdown by concept type
    breakdown = {}
    base_concept = apps.get_model(app_label='transactions', model_name='BaseConcept')
    all_concepts = base_concept.objects.filter(transaction__in=transaction_set)
    for concept in all_concepts:

        # Update existing concept type total
        if concept.concept_type in breakdown:
            # Add value
            breakdown[concept.concept_type].values.append(concept.value)
            breakdown[concept.concept_type].concept_count += 1

        # Start new concept type total
        else:
            breakdown[concept.concept_type] = BreakdownType(concept.child._meta.verbose_name_plural, [concept.value], 1, None)

    for concept_type in breakdown:
        breakdown[concept_type].totals = get_value_totals(breakdown[concept_type].values)

    return [value for _, value in breakdown.items()]


def get_breakdown_by_user(transaction_set):
    """

    :param transaction_set: A set of transactions
    :return: A list of objects with the breakdown
    """
    pass


def get_deposits_in_holding(transaction_set):
    """

    :param transaction_set: A set of transactions
    :return: A list of objects with the breakdown
    """

    accounting_group = 'Deposits'
    breakdown = {}

    # For each concept type in the Deposits accounting group
    for concept_model_name in settings.CONCEPTS:
        concept_model = apps.get_model(concept_model_name)
        if concept_model().settings.accounting_group == accounting_group:

            all_concepts = concept_model.objects.filter(
                transaction__in=transaction_set,
            )
            #import pdb;pdb.set_trace()
            for concept in all_concepts:

                # Update existing concept type total
                if concept.concept_type in breakdown:
                    # Add value
                    breakdown[concept.concept_type].values.append(concept.value)
                    breakdown[concept.concept_type].concept_count += 1

                # Start new concept type total
                else:
                    breakdown[concept.concept_type] = BreakdownType(concept.child._meta.verbose_name_plural, [concept.value], 1, None)

    # Calculate totals per type
    for concept_type in breakdown:
        breakdown[concept_type].totals = get_value_totals(breakdown[concept_type].values)

    # Calculate global total
    number = 0
    values = []
    for concept_type in breakdown:
        number += breakdown[concept_type].concept_count
        values += breakdown[concept_type].totals
    breakdown['Totals'] = BreakdownType(gettext_lazy('Totals'), values, number, get_value_totals(values))

    return [value for _, value in breakdown.items()]


def get_value_totals(values):
    """
    :return: The totals per currency for the given values
    """

    # A dictionary of currency:value totals to return
    totals = {}

    # For each concept
    for value in values:

        # Update existing currency total
        if value.currency in totals:
            # Add if credit
            if value.credit:
                totals[value.currency].amount += value.amount
            # Subtract if debit
            else:
                totals[value.currency].amount -= value.amount

        # Start new currency total
        else:
            totals[value.currency] = DummyValue(
                amount=value.amount if value.credit else value.amount*(-1),
                credit=True,
                currency=value.currency,
            )

    # Update totals credit value
    for _, value in totals.items():
        if value.amount < 0:
            value.credit = False
            value.amount *= -1

    # Return as ordered list of dummy values
    return [v for v in totals.values()]
