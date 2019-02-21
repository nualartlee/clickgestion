from django.shortcuts import get_object_or_404, redirect, render, reverse
from django.contrib.auth.decorators import login_required
from clickgestion.transactions.models import Transaction
from clickgestion.apt_rentals.models import AptRental, AptRentalDeposit
from clickgestion.apt_rentals.forms import RentalForm
from django.utils.translation import gettext
from clickgestion.transactions.views import concept_new


@login_required()
def rental_new(request, *args, **kwargs):
    extra_context = {}

    # Check permissions

    # Get the transaction
    transaction_code = kwargs.get('transaction_code', None)
    transaction = get_object_or_404(Transaction, code=transaction_code)
    extra_context['transaction'] = transaction

    # Check that the transaction is open
    if transaction.closed:
        return redirect('message', message=gettext('Transaction Closed'))

    # POST
    if request.method == 'POST':
        form = RentalForm(request.POST)
        if form.is_valid():
            AptRental(
                transaction=transaction,
                checkin=form.cleaned_data['checkin'],
                checkout=form.cleaned_data['checkout'],
            ).save()
            return redirect('transaction_edit', transaction_code=transaction.code)

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
    rental = get_object_or_404(AptRental, id=rental_id)
    extra_context['rental'] = rental
    extra_context['transaction'] = rental.transaction

    # Use default delete view
    extra_context['header'] = gettext('Delete {}?'.format(rental.type))
    extra_context['message'] = rental.description_short
    extra_context['next'] = request.META['HTTP_REFERER']

    # POST
    if request.method == 'POST':
        default_next = reverse('transaction_detail', kwargs={'transaction_code': rental.transaction.code})
        rental.delete()
        next_page = request.POST.get('next', default_next)
        return redirect(next_page)

    # GET
    else:
        return render(request, 'core/delete.html', extra_context)


def rental_detail(request, *args, **kwargs):
    extra_context = {}

    # Check permissions

    # Get the rental
    rental_id = kwargs.get('rental_id', None)
    rental = get_object_or_404(AptRental, id=rental_id)
    extra_context['rental'] = rental
    extra_context['transaction'] = rental.transaction
    return render(request, 'apt_rentals/rental_detail.html', extra_context)


@login_required()
def rental_edit(request, *args, **kwargs):
    extra_context = {}

    # Check permissions

    # Get the rental
    rental_id = kwargs.get('rental_id', None)
    rental = get_object_or_404(AptRental, id=rental_id)
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
            return redirect('transaction_edit', transaction_code=rental.transaction.code)

        else:
            extra_context['form'] = form
            return render(request, 'apt_rentals/rental_edit.html', extra_context)

    # GET
    else:

        # Get the form
        form = RentalForm(instance=rental)
        extra_context['form'] = form
        return render(request, 'apt_rentals/rental_edit.html', extra_context)


@login_required()
def deposit_new(request, *args, **kwargs):

    # Set the concept
    kwargs['concept_type'] = AptRentalDeposit().class_type
    # Set the form
    kwargs['concept_form'] = RentalForm
    # Return the default view
    return concept_new(request, *args, **kwargs)


def deposit_delete(request, *args, **kwargs):
    extra_context = {}

    # Check permissions

    # Get the rental
    rental_id = kwargs.get('rental_id', None)
    rental = get_object_or_404(AptRental, id=rental_id)
    extra_context['rental'] = rental
    extra_context['transaction'] = rental.transaction

    # Use default delete view
    extra_context['header'] = gettext('Delete {}?'.format(rental.type))
    extra_context['message'] = rental.description_short
    extra_context['next'] = request.META['HTTP_REFERER']

    # POST
    if request.method == 'POST':
        default_next = reverse('transaction_detail', kwargs={'transaction_code': rental.transaction.code})
        rental.delete()
        next_page = request.POST.get('next', default_next)
        return redirect(next_page)

    # GET
    else:
        return render(request, 'core/delete.html', extra_context)


def deposit_detail(request, *args, **kwargs):
    extra_context = {}

    # Check permissions

    # Get the rental
    rental_id = kwargs.get('rental_id', None)
    rental = get_object_or_404(AptRental, id=rental_id)
    extra_context['rental'] = rental
    extra_context['transaction'] = rental.transaction
    return render(request, 'apt_rentals/rental_detail.html', extra_context)


@login_required()
def deposit_edit(request, *args, **kwargs):
    extra_context = {}

    # Check permissions

    # Get the rental
    rental_id = kwargs.get('rental_id', None)
    rental = get_object_or_404(AptRental, id=rental_id)
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
            return redirect('transaction_edit', transaction_code=rental.transaction.code)

        else:
            extra_context['form'] = form
            return render(request, 'apt_rentals/rental_edit.html', extra_context)

    # GET
    else:

        # Get the form
        form = RentalForm(instance=rental)
        extra_context['form'] = form
        return render(request, 'apt_rentals/rental_edit.html', extra_context)
