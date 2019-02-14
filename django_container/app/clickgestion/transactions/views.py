from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from clickgestion.transactions.models import Transaction
from clickgestion.transactions.forms import TransactionEditForm, TransactionPayForm
from django.utils.translation import gettext
from django.utils import timezone
from clickgestion.transactions.filters import EmployeeFilter
from django.views.generic import ListView
from pure_pagination.mixins import PaginationMixin
from clickgestion.core.utilities import invalid_permission_redirect


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

def transaction_delete(request, *args, **kwargs):
    extra_context = {}

    # Check permissions
    if not request.user.is_authenticated:
        return invalid_permission_redirect(request)

    # Get the object
    transaction_id = kwargs.get('transaction_id', None)
    transaction = get_object_or_404(Transaction, id=transaction_id)
    extra_context['transaction'] = transaction

    # Use default delete view
    extra_context['header'] = gettext('Delete Transaction?')
    extra_context['message'] = transaction.description_short
    extra_context['next'] = request.META['HTTP_REFERER']

    # POST
    if request.method == 'POST':
        default_next = reverse('transactions_open')
        transaction.delete()
        next_page = request.POST.get('next', default_next)
        return redirect(next_page)

    # GET
    else:
        return render(request, 'core/delete.html', extra_context)


@login_required
def transaction_detail(request, *args, **kwargs):
    extra_context = {}

    # Check permissions
    if not request.user.is_authenticated:
        return invalid_permission_redirect(request)

    # Get the transaction
    transaction_id = kwargs.get('transaction_id', None)
    transaction = get_object_or_404(Transaction, id=transaction_id)
    extra_context['transaction'] = transaction
    return render(request, 'transactions/transaction_detail.html', extra_context)


@login_required
def transaction_edit(request, *args, **kwargs):
    extra_context = {}

    # Check permissions
    if not request.user.is_authenticated:
        return invalid_permission_redirect(request)

    # Get the transaction
    transaction_id = kwargs.get('transaction_id', None)
    transaction = get_object_or_404(Transaction, id=transaction_id)
    extra_context['transaction'] = transaction

    # Check that the transaction is open
    if transaction.closed:
        return redirect('message', message=gettext('Transaction Closed'))

    # Get available concepts to add
    available_concepts = get_available_concepts(request.user, transaction)
    extra_context['available_concepts'] = available_concepts

    # POST
    if request.method == 'POST':
        form = TransactionEditForm(request.POST, instance=transaction)
        valid = form.is_valid()

        # Delete and go home
        # Note that the form.data value is still a string before validating
        if form.data['cancel_button'] == 'True':
            transaction.delete()
            return redirect('index')

        # If valid
        if valid:

            # Save the transaction
            transaction.save()

            # Finish later
            if form.cleaned_data['save_button']:
                return redirect('transaction_detail', transaction_id=transaction.id)

            # Proceed to pay
            return redirect('transaction_pay', transaction_id=transaction.id)

        else:
            extra_context['form'] = form
            return render(request, 'transactions/transaction_edit.html', extra_context)

    # GET
    else:

        # Create the form
        form = TransactionEditForm(instance=transaction)
        extra_context['form'] = form
        return render(request, 'transactions/transaction_edit.html', extra_context)


class TransactionList(PaginationMixin, ListView):

    model = Transaction
    context_object_name = 'transactions'
    paginate_by = 10
    queryset = None
    header = gettext('Transactions')
    request = None
    filter = None

    def get(self, request, *args, **kwargs):

        # Check permissions
        if not request.user.is_authenticated:
            return invalid_permission_redirect(request)

        self.request = request
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Call the base implementation first
        context = super().get_context_data(**kwargs)

        # Add data
        context['header'] = self.header
        context['filter'] = self.filter

        return context

    def get_queryset(self):
        if not self.queryset:
            self.queryset = Transaction.objects.all()
        # Filter
        self.filter = EmployeeFilter(self.request.GET, queryset=self.queryset)
        self.queryset = self.filter.qs
        return self.queryset


@login_required()
def transaction_new(request, *args, **kwargs):
    extra_context = {}

    # Check permissions
    if not request.user.is_authenticated:
        return invalid_permission_redirect(request)

    # Create the transaction
    transaction = Transaction.objects.create(
        employee=request.user,
    )
    extra_context['transaction'] = transaction

    # Redirect to edit
    return redirect('transaction_edit', transaction_id=transaction.id)


@login_required
def transaction_pay(request, *args, **kwargs):
    extra_context = {}

    # Check permissions
    if not request.user.is_authenticated:
        return invalid_permission_redirect(request)

    # Get the transaction
    transaction_id = kwargs.get('transaction_id', None)
    transaction = get_object_or_404(Transaction, id=transaction_id)
    extra_context['transaction'] = transaction

    # Check that the transaction is open
    if transaction.closed:
        return redirect('message', message=gettext('Transaction Closed'))

    # Get required payment fields

    # POST
    if request.method == 'POST':
        form = TransactionPayForm(request.POST, instance=transaction)
        valid = form.is_valid()

        # If cancel has been set, delete and go home
        # Note that value is still string before validating
        if form.data['cancel_button'] == 'True':
            transaction.delete()
            return redirect('index')

        # If valid
        if valid:

            # Close the transaction
            if form.cleaned_data['confirm_button']:
                transaction.closed = True
                transaction.closed_time = timezone.datetime.now()
                transaction.save()
                return redirect('transaction_detail', transaction_id=transaction.id)

            # Save the transaction
            if form.cleaned_data['save_button']:
                transaction.save()
                return redirect('transaction_detail', transaction_id=transaction.id)

        else:
            extra_context['form'] = form
            return render(request, 'transactions/transaction_pay.html', extra_context)

    # GET
    else:

        # Create the form
        form = TransactionPayForm(instance=transaction)
        extra_context['form'] = form
        return render(request, 'transactions/transaction_pay.html', extra_context)


def transactions_open(request, *args, **kwargs):

    # Check permissions
    if not request.user.is_authenticated:
        return invalid_permission_redirect(request)

    # Get queryset
    queryset = Transaction.objects.filter(employee=request.user, closed=False)

    # Set header
    header = gettext('Open transactions by %(employee)s' % {'employee': request.user})

    # Return
    listview = TransactionList.as_view(queryset=queryset, header=header)
    return listview(request)
