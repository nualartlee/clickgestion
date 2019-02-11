from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from clickgestion.transactions.models import Transaction
from clickgestion.apt_rentals.models import ApartmentRental
from clickgestion.apt_rentals.forms import RentalForm
from django.utils.translation import gettext


@login_required()
def rental_new(request, *args, **kwargs):
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

        # Get the form
        rental_form = RentalForm()
        extra_context['rental_form'] = rental_form
        return render(request, 'apt_rentals/rental_new.html', extra_context)


