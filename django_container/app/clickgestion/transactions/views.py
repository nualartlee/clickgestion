from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from clickgestion.transactions.models import Transaction
from clickgestion.transactions.forms import TransactionForm
from django.utils.translation import gettext


def get_available_concepts(employee, transaction):
    """
    Get a list of the available concepts that can be added to the given transaction.

    :param employee: The employee executing the transaction (current user)
    :param transaction: The open transaction
    :return: A list of dictionaries.
    """
    concepts = []
    apt_rental = {
        'name': gettext('Apartment Rental'),
        'url': '/apt-rentals/new/{}'.format(transaction.id),
    }
    concepts.append(apt_rental)
    return concepts


@login_required
def transaction_detail(request, *args, **kwargs):
    extra_context = {}

    # Check permissions

    # Get the transaction
    transaction_id = kwargs.get('transaction_id', None)
    transaction = get_object_or_404(Transaction, id=transaction_id)
    extra_context['transaction'] = transaction
    return render(request, 'transactions/transaction_detail.html', extra_context)


@login_required
def transaction_edit(request, *args, **kwargs):
    extra_context = {}

    # Check permissions

    # Get the transaction
    transaction_id = kwargs.get('transaction_id', None)
    transaction = get_object_or_404(Transaction, id=transaction_id)
    extra_context['transaction'] = transaction

    # Check that the transaction is open
    if transaction.closed:
        return redirect('message', message=gettext('Transaction Closed'))

    # POST
    if request.method == 'POST':

        return redirect('login')

    # GET
    else:

        # Get available concepts to add
        available_concepts = get_available_concepts(request.user, transaction)
        extra_context['available_concepts'] = available_concepts

        # Get the form
        transaction_form = TransactionForm()
        extra_context['transaction_form'] = transaction_form
        return render(request, 'transactions/transaction_edit.html', extra_context)


@login_required()
def transaction_new(request, *args, **kwargs):
    extra_context = {}

    # Check permissions

    # Create the transaction
    transaction = Transaction.objects.create(
        employee=request.user,
    )
    extra_context['transaction'] = transaction

    # Redirect to edit
    return redirect('transaction_edit', transaction_id=transaction.id)
