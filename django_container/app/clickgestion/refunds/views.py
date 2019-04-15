from django.apps import apps
from django.shortcuts import get_object_or_404, redirect
from django.utils.translation import gettext
from django.contrib.auth.decorators import login_required
from clickgestion.core.views import message
from django.core.exceptions import ObjectDoesNotExist
from clickgestion.refunds.models import Refund
import urllib

"""
For future use

from clickgestion.refunds.filters import RefundFilter
class RefundList(ConceptList):

    # ListView.as_view will pass custom arguments here
    queryset = None
    header = gettext('Refunds')
    request = None
    filter_type = RefundFilter
    filter = None
    filter_data = None
    is_filtered = False
    
"""


@login_required()
def refund_new(request, *args, **kwargs):
    extra_context = {}

    # Check for a concept to refund
    concept_code = kwargs.get('concept_code', None)
    if concept_code:
        concept = get_object_or_404(apps.get_model('concepts.BaseConcept'), code=concept_code)

        # Check that the concept is refundable
        if not concept.can_refund:
            extra_context['header'] = gettext('Error')
            extra_context['message'] = gettext('Cannot refund {}'.format(concept.description_short))
            return message(request, extra_context)

        # Check for a transaction waiting for the concept to refund
        transaction_code = request.session.pop('refund_transaction_code', None)
        try:
            transaction = apps.get_model('transactions.Transaction').objects.get(code=transaction_code)
        except ObjectDoesNotExist:
            # Create the transaction if not provided
            transaction_model = apps.get_model('transactions.Transaction')
            transaction = transaction_model()

        # Copy client data from refunded concept
        transaction.apt_number = concept.transaction.apt_number
        transaction.client_address = concept.transaction.client_address
        transaction.client_email = concept.transaction.client_email
        transaction.client_first_name = concept.transaction.client_first_name
        transaction.client_id = concept.transaction.client_id
        transaction.client_last_name = concept.transaction.client_last_name
        transaction.client_phone_number = concept.transaction.client_phone_number
        transaction.employee = request.user
        transaction.save()

        # Delete any open refunds
        concept.refunds.all().delete()

        # Create the return
        Refund(transaction=transaction, refunded_concept=concept).save()

        # Redirect to transaction edit
        return redirect('transaction_edit', transaction_code=transaction.code)

    # Check for a transaction to add a return to
    transaction_code = kwargs.get('transaction_code', None)
    if transaction_code:
        transaction = get_object_or_404(apps.get_model('transactions.Transaction'), code=transaction_code)

        # Save the transaction in cookie before looking for the deposit to return
        request.session['refund_transaction_code'] = transaction.code

        # Set initial filter data and display refundable list
        filter_data = {
            'refund_status': False,
        }
        params = urllib.parse.urlencode(filter_data)
        # Return
        response = redirect('concept_list')
        response['Location'] += '?{}'.format(params)
        return response
