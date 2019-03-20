from django.apps import apps
from clickgestion.concepts.views import ConceptList
from clickgestion.deposits.filters import DepositFilter
from clickgestion.deposits.models import DepositReturn
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import urllib
from django.utils.translation import gettext


def depositreturns_today(request, *args, **kwargs):

    # Set initial filter data
    filter_data = {
        'end_date_after': timezone.localdate(),
        'end_date_before': timezone.localdate(),
        'returned': False,
    }
    params = urllib.parse.urlencode(filter_data)
    # Return
    response = redirect('deposit_list')
    response['Location'] += '?{}'.format(params)
    return response


class DepositList(ConceptList):

    # ListView.as_view will pass custom arguments here
    queryset = None
    header = gettext('Deposits')
    request = None
    filter_type = DepositFilter
    filter = None
    filter_data = None
    is_filtered = False


@login_required()
def depositreturn_new(request, *args, **kwargs):
    extra_context = {}

    # Check for a concept to return
    concept_code = kwargs.get('concept_code', None)
    if concept_code:
        concept = get_object_or_404(apps.get_model('concepts.BaseConcept'), code=concept_code)

        # Check that the concept is a returnable deposit
        if not concept.can_return_deposit:
            extra_context['header'] = gettext('Error')
            extra_context['message'] = gettext('Cannot return {}'.format(concept.description_short))
            return redirect('message')

        # Check for a transaction waiting for the concept to return
        transaction_code = request.session.pop('depositreturn_transaction_code', None)
        if transaction_code:
            transaction = get_object_or_404(apps.get_model('transactions.Transaction'), code=transaction_code)

        # Create the transaction if not provided
        else:
            transaction_model = apps.get_model('transactions.Transaction')
            transaction = transaction_model()

        # Copy client data from deposit
        transaction.apt_number = concept.transaction.apt_number
        transaction.client_address = concept.transaction.client_address
        transaction.client_email = concept.transaction.client_email
        transaction.client_first_name = concept.transaction.client_first_name
        transaction.client_id = concept.transaction.client_id
        transaction.client_last_name = concept.transaction.client_last_name
        transaction.client_phone_number = concept.transaction.client_phone_number
        transaction.employee = request.user
        transaction.save()

        # Delete any open returns
        concept.depositreturns.all().delete()

        # Create the return
        DepositReturn(transaction=transaction, returned_deposit=concept).save()

        # Redirect to transaction edit
        return redirect('transaction_edit', transaction_code=transaction.code)

    # Check for a transaction to add a return to
    transaction_code = kwargs.get('transaction_code', None)
    if transaction_code:
        transaction = get_object_or_404(apps.get_model('transactions.Transaction'), code=transaction_code)

        # Save the transaction in cookie before looking for the deposit to return
        request.session['depositreturn_transaction_code'] = transaction.code

        # Set initial filter data and display returnable deposit list
        filter_data = {
            'returned': False,
        }
        params = urllib.parse.urlencode(filter_data)
        # Return
        response = redirect('deposit_list')
        response['Location'] += '?{}'.format(params)
        return response
