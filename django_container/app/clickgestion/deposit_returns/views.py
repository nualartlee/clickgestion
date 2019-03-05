from django.apps import apps
from clickgestion.cash_desk.forms import CashCloseForm
from clickgestion.transactions.models import Transaction
from clickgestion.transactions import totalizers
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.utils.translation import gettext, gettext_lazy
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone


@login_required()
def deposit_return_new(request, *args, **kwargs):
    extra_context = {}

    # Get deposits to be returned today
    accounting_group = 'Deposits'

    # For each concept type in the Deposits accounting group
    deposit_types = []
    for concept_model_name in settings.CONCEPTS:
        concept_model = apps.get_model(concept_model_name)
        if concept_model().settings.accounting_group == accounting_group:
            deposit_type = {}
            deposit_type['type'] = concept_model().concept_type
            deposit_type['concepts'] = concept_model.objects.filter(
                transaction__closed=True,
                return_date__year=timezone.now().year,
                return_date__month=timezone.now().month,
                return_date__day=timezone.now().day,
                deposit_return=None,
            )
            deposit_types.append(deposit_type)
    extra_context['deposit_types'] = deposit_types
    return render(request, 'deposits/cash_desk_close.html', extra_context)

