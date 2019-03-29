from django.apps import apps
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy
from django.db.models import Sum

User = get_user_model()


class ConceptGroupTotal:
    """
    Contains the description and total of a group of concepts for display
    """
    def __init__(self, name, concepts, concept_count, totals):
        self.name = name
        self.concepts = concepts
        self.concept_count = concept_count
        self.totals = totals


class DummyValue:
    """
    Dummy ConceptValue for display
    """
    def __init__(self, amount, credit, currency):
        self.amount = amount
        self.credit = credit
        self.currency = currency


def get_breakdown_by_accounting_group(concepts='__all__'):
    """
    Totalize the given concepts according to the accounting group

    :param concepts: The queryset of concepts to totalize
    :return: a list of ConceptGroupTotals
    """
    # Concept models
    base_concept = apps.get_model('concepts.BaseConcept')
    concept_value = apps.get_model('concepts.ConceptValue')

    # Get the concepts if not provided
    if concepts == '__all__':
       concepts = base_concept.objects.filter(transaction__closed=True).prefetch_related('value__currency')

    # Get the distinct accounting groups
    groups = [item[0] for item in concepts.values_list('accounting_group').order_by('accounting_group').distinct()]

    # Create a list to hold the concept totals
    breakdown = []

    # Select by group
    for group in [g for g in groups if g]:
        group_total = ConceptGroupTotal(
            name=gettext_lazy(group),
            concepts=concepts.filter(accounting_group=group).prefetch_related('value__currency'),
            concept_count=None,
            totals=None,
        )
        group_total.concept_count = group_total.concepts.count()
        group_total.totals = get_value_totals(group_total.concepts)
        breakdown.append(group_total)

    # Return the list of totals
    return breakdown


def get_breakdown_by_concept_type(concepts='__all__'):
    """
    Totalize the given concepts according to concept type

    :param concepts: The queryset of concepts to totalize
    :return: a list of ConceptGroupTotals
    """
    # Concept models
    base_concept = apps.get_model('concepts.BaseConcept')
    concept_value = apps.get_model('concepts.ConceptValue')

    # Get the concepts if not provided
    if concepts == '__all__':
        concepts = base_concept.objects.filter(transaction__closed=True).prefetch_related('value__currency')

    # Get the distinct concept types
    groups = [item[0] for item in concepts.values_list('concept_name').order_by('concept_name').distinct()]

    # Create a list to hold the concept totals
    breakdown = []

    # Select by group
    for group in [g for g in groups if g]:
        group_total = ConceptGroupTotal(
            #name=gettext_lazy(group),
            name=None,
            concepts=concepts.filter(concept_name=group).prefetch_related('value__currency'),
            concept_count=None,
            totals=None,
        )
        group_total.concept_count = group_total.concepts.count()
        group_total.totals = get_value_totals(group_total.concepts)
        group_total.name = group_total.concepts[0].name_plural
        breakdown.append(group_total)

    # Return the list of totals
    return breakdown


def get_breakdown_by_employee(concepts='__all__'):
    """

    :param concepts: The queryset of concepts to totalize
    :return: a list of ConceptGroupTotals
    """
    # Concept models
    base_concept = apps.get_model('concepts.BaseConcept')
    concept_value = apps.get_model('concepts.ConceptValue')

    # Get the concepts if not provided
    if concepts == '__all__':
        concepts = base_concept.objects.filter(transaction__closed=True).prefetch_related('value__currency')

    # Get the distinct employees
    groups = [item[0] for item in concepts.values_list('transaction__employee').order_by('transaction__employee').distinct()]

    # Create a list to hold the concept totals
    breakdown = []

    # Select by group
    for group in [g for g in groups if g]:
        group_total = ConceptGroupTotal(
            name=User.objects.get(id=group).get_full_name(),
            concepts=concepts.filter(transaction__employee=group).prefetch_related('value__currency'),
            concept_count=None,
            totals=None,
        )
        group_total.concept_count = group_total.concepts.count()
        group_total.totals = get_value_totals(group_total.concepts)
        breakdown.append(group_total)

    # Return the list of totals
    return breakdown


def get_deposits_in_holding(concepts='__all__'):
    """

    :param concepts: The queryset of concepts to totalize
    :return: a list of ConceptGroupTotals
    """
    # Concept models
    base_concept = apps.get_model('concepts.BaseConcept')
    accounting_group = 'Deposits'

    # Get the concepts if not provided
    if concepts == '__all__':
        # No deposit return concept
        holding1 = base_concept.objects.filter(
            accounting_group=accounting_group,
            transaction__closed=True,
            depositreturns=None,
        ).prefetch_related('value__currency')
        # Deposit return concept opened
        holding2 = base_concept.objects.filter(
            accounting_group=accounting_group,
            transaction__closed=True,
            depositreturns__transaction__closed=False,
        ).prefetch_related('value__currency')
        # Query union
        concepts = holding1 | holding2

    # Return as breakdown
    return get_breakdown_by_concept_type(concepts)


def get_value_totals(concepts):
    """
    Get the total amount per currency of a given queryset of concepts

    :param concepts: BaseConcept queryset to totalize
    :return: A list of DummyValues, one per currency
    """
    # models
    concept_value = apps.get_model('concepts.ConceptValue')
    currency_model = apps.get_model('concepts.Currency')

    # The list of DummyValues to return
    totals = []

    # Get the values
    values = concept_value.objects.filter(concept__in=concepts).prefetch_related('currency')

    # Get distinct currencies
    currencies = currency_model.objects.filter(values__in=values).order_by('id').distinct()

    # Totalize per currency
    for currency in currencies:
        cr = values.filter(currency=currency, credit=True).aggregate(Sum('amount'))['amount__sum'] or 0
        db = values.filter(currency=currency, credit=False).aggregate(Sum('amount'))['amount__sum'] or 0
        amount = cr - db
        credit = amount >= 0
        currency_total = DummyValue(
            amount=abs(amount),
            credit=credit,
            currency=currency,
        )
        totals.append(currency_total)

    # Return the list of DumyValues
    return totals

