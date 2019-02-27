from django.shortcuts import render, redirect, reverse, get_object_or_404
from itertools import chain
from django.contrib.auth.decorators import login_required
from clickgestion.transactions.models import Transaction, get_breakdown_by_concept_type, get_value_totals
from clickgestion.transactions.forms import TransactionEditForm, TransactionPayForm
from django.utils.translation import gettext, gettext_lazy
from django.utils import timezone
from clickgestion.transactions.filters import EmployeeFilter
from django.views.generic import ListView
from pure_pagination.mixins import PaginationMixin
from clickgestion.core.utilities import invalid_permission_redirect
from django.contrib.auth.models import Group, Permission


@login_required()
def cash_balance(request, *args, **kwargs):
    extra_context = {}

    # Get closed transactions
    transactions = Transaction.objects.filter(closed=True, cashclose=None)
    extra_context['transactions'] = transactions

    # Get breakdown by concept type
    breakdown = get_breakdown_by_concept_type(transactions)
    extra_context['breakdown'] = breakdown

    # Get the totals
    values = []
    for transaction in transactions:
        values += transaction.totals
    totals = get_value_totals(values)
    extra_context['totals'] = totals

    # Render
    return render(request, 'transactions/cash_balance.html', extra_context)





@login_required()
def concept_delete(request, *args, **kwargs):
    extra_context = {}

    # Check permissions

    # Get the concept and form
    concept, concept_form = get_concept_and_form_from_kwargs(**kwargs)
    extra_context['concept'] = concept

    # Get the transaction
    transaction = concept.transaction
    if transaction.closed:
        return redirect('message', message=gettext('Transaction Closed'))
    extra_context['transaction'] = transaction

    # Use default delete view
    extra_context['header'] = gettext('Delete {}?'.format(concept.concept_type))
    extra_context['message'] = concept.description_short
    extra_context['next'] = request.META['HTTP_REFERER']

    # POST
    if request.method == 'POST':
        default_next = reverse('transaction_detail', kwargs={'transaction_code': concept.transaction.code})
        concept.delete()
        next_page = request.POST.get('next', default_next)
        return redirect(next_page)

    # GET
    else:
        return render(request, 'core/delete.html', extra_context)


@login_required()
def concept_detail(request, *args, **kwargs):
    extra_context = {}

    # Check permissions

    # Get the concept and form
    concept, concept_form = get_concept_and_form_from_kwargs(**kwargs)
    extra_context['concept'] = concept

    # Get the transaction
    transaction = concept.transaction
    extra_context['transaction'] = transaction

    return render(request, 'transactions/concept_detail.html', extra_context)


@login_required()
def concept_edit(request, *args, **kwargs):
    extra_context = {}

    # Check permissions

    # Get the concept and form
    concept, concept_form = get_concept_and_form_from_kwargs(**kwargs)
    extra_context['concept'] = concept

    # Get the transaction
    transaction = concept.transaction
    if transaction.closed:
        return redirect('message', message=gettext('Transaction Closed'))
    extra_context['transaction'] = transaction

    # POST
    if request.method == 'POST':
        form = concept_form(request.POST, instance=concept)
        if form.is_valid():
            form.save()
            return redirect('transaction_edit', transaction_code=transaction.code)

        else:
            extra_context['form'] = form
            return render(request, 'transactions/concept_edit.html', extra_context)

    # GET
    else:

        # Get the form
        form = concept_form(instance=concept)
        extra_context['form'] = form
        return render(request, 'transactions/concept_edit.html', extra_context)


def get_available_concepts(employee, transaction):
    """
    Get a list of the available concepts that can be added to the given transaction.

    :param employee: The employee executing the transaction (current user)
    :param transaction: The open transaction
    :return: A list of dictionaries.
    """
    from clickgestion.apt_rentals.models import AptRental, AptRentalDeposit
    from clickgestion.cash_float.models import CashFloatDeposit, CashFloatWithdrawal
    all_concepts = [AptRental, AptRentalDeposit, CashFloatDeposit, CashFloatWithdrawal]


    # get current transaction concepts
    concepts = transaction.concepts.all()
    if concepts.count() > 0:
        # get permission groups from current concepts
        concept_groups = list(
            chain(concept.settings.permission_group for concept in concepts)
        )
        # get all permissions from current concepts
        concept_permissions = Permission.objects.filter(group__in=concept_groups)
        # get permissions as a list of model classes
        concept_permission_models = list(chain(permission.content_type.model_class() for permission in concept_permissions))
    else:
        concept_permission_models = all_concepts

    concept_list = []
    for concept in all_concepts:
        # set default values
        disabled = False
        url = concept._url.format('new/{}'.format(transaction.code))
        # filter by selected concepts
        if not concept in concept_permission_models:
            disabled = True
            url = '#'
        concept_list.append(
            {
                'name': concept._meta.verbose_name,
                'url': url,
                'disabled': disabled,
            }
        )

    return concept_list


def get_transaction_from_kwargs(**kwargs):
    # Get the transaction
    transaction_code = kwargs.get('transaction_code', None)
    transaction = get_object_or_404(Transaction, code=transaction_code)
    return transaction


def get_concept_and_form_from_kwargs(**kwargs):

    # Get the form
    concept_form = kwargs.get('concept_form', None)

    # Get the concept class
    concept_class = concept_form._meta.model

    # If a transaction code is provided, this is a new concept
    transaction_code = kwargs.get('transaction_code', None)
    if transaction_code:
        transaction = get_transaction_from_kwargs(**kwargs)
        return concept_class(transaction=transaction), concept_form

    # Get the existing concept
    concept_code = kwargs.get('concept_code', None)
    concept = get_object_or_404(concept_class, code=concept_code)
    return concept, concept_form


def transaction_delete(request, *args, **kwargs):
    extra_context = {}

    # Check permissions
    if not request.user.is_authenticated:
        return invalid_permission_redirect(request)

    # Get the object
    transaction_code = kwargs.get('transaction_code', None)
    transaction = get_object_or_404(Transaction, code=transaction_code)
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
    transaction_code = kwargs.get('transaction_code', None)
    transaction = get_object_or_404(Transaction, code=transaction_code)
    extra_context['transaction'] = transaction
    return render(request, 'transactions/transaction_detail.html', extra_context)


@login_required
def transaction_edit(request, *args, **kwargs):
    extra_context = {}

    # Check permissions
    if not request.user.is_authenticated:
        return invalid_permission_redirect(request)

    # Get the transaction
    transaction_code = kwargs.get('transaction_code', None)
    transaction = get_object_or_404(Transaction, code=transaction_code)
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
                return redirect('transaction_detail', transaction_code=transaction.code)

            # Proceed to pay
            return redirect('transaction_pay', transaction_code=transaction.code)

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
    header = None
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
        if not self.header:
            header = gettext_lazy('Transactions')
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
    return redirect('transaction_edit', transaction_code=transaction.code)


@login_required
def transaction_pay(request, *args, **kwargs):
    extra_context = {}

    # Check permissions
    if not request.user.is_authenticated:
        return invalid_permission_redirect(request)

    # Get the transaction
    transaction_code = kwargs.get('transaction_code', None)
    transaction = get_object_or_404(Transaction, code=transaction_code)
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
                transaction.closed_date = timezone.datetime.now()
                transaction.save()
                return redirect('transaction_detail', transaction_code=transaction.code)

            # Save the transaction
            if form.cleaned_data['save_button']:
                transaction.save()
                return redirect('transaction_detail', transaction_code=transaction.code)

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
    header = gettext_lazy('Pending transactions by %(employee)s' % {'employee': request.user})

    # Return
    listview = TransactionList.as_view(queryset=queryset, header=header)
    return listview(request)
