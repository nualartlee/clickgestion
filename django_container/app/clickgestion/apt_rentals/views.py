from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.decorators import login_required
from clickgestion.transactions.models import Transaction
from clickgestion.apt_rentals.models import ApartmentRental
from clickgestion.apt_rentals.forms import RentalForm
from django.utils.translation import gettext
from clickgestion.core.forms import CoreBackForm, CoreDeleteForm


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
        form = RentalForm(request.POST)
        if form.is_valid():
            ApartmentRental(
                transaction=transaction,
                checkin=form.cleaned_data['checkin'],
                checkout=form.cleaned_data['checkout'],
            ).save()
            return redirect('transaction_edit', transaction_id=transaction.id)

        else:
            extra_context['form'] = form
            return render(request, 'apt_rentals/rental_edit.html', extra_context)

    # GET
    else:

        # Get the form
        form = RentalForm()
        extra_context['form'] = form
        return render(request, 'apt_rentals/rental_edit.html', extra_context)


def rental_delete(request, *args, **kwargs):
    extra_context = {}

    # Check permissions

    # Get the rental
    rental_id = kwargs.get('rental_id', None)
    rental = get_object_or_404(ApartmentRental, id=rental_id)
    extra_context['rental'] = rental
    extra_context['transaction'] = rental.transaction

    # Use default views
    extra_context['header'] = gettext('Delete {}?'.format(rental.type))
    extra_context['message'] = rental.description_short
    referer = request.META['HTTP_REFERER']
    extra_context['form'] = CoreDeleteForm(referer=referer)

    # POST
    if request.method == 'POST':
        default_next = reverse('transaction_detail', kwargs={'transaction_id': rental.transaction.id})
        rental.delete()
        next_page = request.POST.get('next', default_next)
        return redirect(next_page)

    # GET
    else:
        return render(request, 'core/message.html', extra_context)


def rental_detail(request, *args, **kwargs):
    extra_context = {}

    # Check permissions

    # Get the rental
    rental_id = kwargs.get('rental_id', None)
    rental = get_object_or_404(ApartmentRental, id=rental_id)
    extra_context['rental'] = rental
    extra_context['transaction'] = rental.transaction
    return render(request, 'apt_rentals/rental_detail.html', extra_context)


@login_required()
def rental_edit(request, *args, **kwargs):
    extra_context = {}

    # Check permissions

    # Get the rental
    rental_id = kwargs.get('rental_id', None)
    rental = get_object_or_404(ApartmentRental, id=rental_id)
    extra_context['rental'] = rental
    extra_context['transaction'] = rental.transaction

    # Check that the transaction is open
    if rental.transaction.closed:
        return redirect('message', message=gettext('Transaction Closed'))

    # POST
    if request.method == 'POST':
        form = RentalForm(request.POST, instance=rental)
        if form.is_valid():
            form.save()
            return redirect('transaction_edit', transaction_id=rental.transaction.id)

        else:
            extra_context['form'] = form
            return render(request, 'apt_rentals/rental_edit.html', extra_context)

    # GET
    else:

        # Get the form
        form = RentalForm(instance=rental)
        extra_context['form'] = form
        return render(request, 'apt_rentals/rental_edit.html', extra_context)
