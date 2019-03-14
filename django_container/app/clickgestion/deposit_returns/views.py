from django.apps import apps
from clickgestion.deposit_returns.models import DepositReturn
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.utils import timezone
from clickgestion.core.utilities import invalid_permission_redirect
import urllib
from clickgestion.transactions.views import get_concept_and_form_from_kwargs
from django.utils.translation import gettext


def today(request, *args, **kwargs):

    # Check permissions
    if not request.user.is_authenticated:
        return invalid_permission_redirect(request)

    # Set initial filter data
    accounting_group = 'Deposits'
    filter_data = {
        'accounting_group': accounting_group,
        'transaction__closed': True,
        'deposit_return': None,
        'end_date_after': timezone.localdate(),
        'end_date_before': timezone.localdate(),
    }
    params = urllib.parse.urlencode(filter_data)
    # Return
    response = redirect('concept_list')
    response['Location'] += '?{}'.format(params)
    return response


@login_required()
def deposit_return(request, *args, **kwargs):
    extra_context = {}

    # Check permissions

    # Get the concept and form
    concept, concept_form = get_concept_and_form_from_kwargs(**kwargs)
    extra_context['concept'] = concept

    # Get the transaction
    transaction = concept.transaction
    extra_context['transaction'] = transaction

    return render(request, 'concepts/concept_detail.html', extra_context)


@login_required()
def deposit_return_new(request, *args, **kwargs):
    extra_context = {}

    # Check for a concept to return
    concept_code = kwargs.get('concept_code', None)
    concept = get_object_or_404(apps.get_model('concepts.BaseConcept'), code=concept_code)

    if concept:

        # Check that the concept is a returnable deposit
        if not concept.can_return_deposit:
            extra_context['header'] = gettext('Error')
            extra_context['message'] = gettext('Cannot return {}'.format(concept.description_short))
            return redirect('message')

        # Check for a transaction waiting for the concept to return
        transaction = request.session.pop('deposit_return_transaction', None)

        # Create the transaction if not provided
        if not transaction:
            Transaction = apps.get_model('transactions.Transaction')
            transaction = Transaction(employee=request.user)
            transaction.save()

        # Create the return
        DepositReturn(transaction=transaction, returned_deposit=concept).save()

        # Redirect to transaction edit
        return redirect('transaction_edit', transaction_code=transaction.code)


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

