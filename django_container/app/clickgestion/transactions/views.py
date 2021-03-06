from django.apps import apps
from clickgestion.core.utilities import custom_permission_required
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.utils.translation import gettext
from django.http import QueryDict
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from pure_pagination.mixins import PaginationMixin
from django.conf import settings
from django.utils import timezone
from clickgestion.transactions.models import Transaction
from clickgestion.transactions.forms import TransactionEditForm, TransactionPayForm
from clickgestion.transactions.filters import TransactionFilter
import urllib


def clear_transaction_session_data(session, transaction):
    """
    Clear any session data related to the given transaction

    :param session: The session to clear
    :param transaction: The transaction
    """
    name = 'depositreturn_transaction_code'
    code = session.get(name, False)
    if transaction.code == code:
        session.pop(name)
    name = 'refund_transaction_code'
    code = session.get(name, False)
    if transaction.code == code:
        session.pop(name)


def get_available_concepts(employee, transaction):
    """
    Get a list of the available concepts that can be added to the given transaction.

    :param employee: The employee executing the transaction (current user)
    :param transaction: The open transaction
    :return: A list of dictionaries.
    """

    # get permissions according to transaction
    concepts_permitted_by_transaction = transaction.get_all_permissions()

    # get permissions according to employee
    concepts_permitted_by_employee = employee.get_all_permissions()

    # create the list of permitted concepts
    available_concepts = []
    for concept in settings.CONCEPTS:
        permission = concept.replace('.', '.add_')
        concept_model = apps.get_model(concept)

        # Skip this concept if not permitted by the user
        if not permission in concepts_permitted_by_employee:
            continue

        # set default values
        disabled = False
        url = concept_model._url.format('new/{}'.format(transaction.code))

        # disable this concept if not permitted by the transaction
        if not permission in concepts_permitted_by_transaction:
            disabled = True
            url = '#'

        # add to the list
        available_concepts.append(
            {
                'name': concept_model._meta.verbose_name,
                'url': url,
                'disabled': disabled,
            }
        )

    return available_concepts


def get_transaction_from_kwargs(**kwargs):
    # Get the transaction
    transaction_code = kwargs.get('transaction_code', None)
    transaction = get_object_or_404(
        Transaction.objects.prefetch_related('concepts__value__currency'),
        code=transaction_code)
    return transaction


@login_required
def transaction_actions(request, *args, **kwargs):
    extra_context = {}

    # Get the transaction
    transaction = get_transaction_from_kwargs(**kwargs)
    extra_context['transaction'] = transaction

    # Return
    return render(request, 'transactions/transaction_actions.html', extra_context)


@login_required
def transaction_concepts(request, *args, **kwargs):

    # Get the transaction
    transaction = get_transaction_from_kwargs(**kwargs)

    # Set initial filter data
    filter_data = {
        'code': transaction.code,
    }
    params = urllib.parse.urlencode(filter_data)
    # Return
    response = redirect('concept_list')
    response['Location'] += '?{}'.format(params)
    return response


@custom_permission_required('transactions.add_transaction')
def transaction_delete(request, *args, **kwargs):
    extra_context = {}

    # Get the transaction
    transaction = get_transaction_from_kwargs(**kwargs)
    extra_context['transaction'] = transaction

    # Check that the transaction is open
    if transaction.closed:
        extra_context['message'] = gettext('Transaction Closed')
        return render(request, 'core/message.html', extra_context)

    # Use default delete view
    extra_context['header'] = gettext('Delete Transaction?')
    extra_context['message'] = transaction.description_short
    extra_context['next'] = request.META.get('HTTP_REFERER', '/')

    # POST
    if request.method == 'POST':

        # Clear session data related to this transaction
        clear_transaction_session_data(request.session, transaction)

        # Delete the transaction
        transaction.delete()

        # Return
        next_page = request.POST.get('next', reverse('transactions_open'))
        return redirect(next_page)

    # GET
    else:
        return render(request, 'core/delete.html', extra_context)


@login_required
def transaction_detail(request, *args, **kwargs):
    extra_context = {}

    # Get the transaction
    transaction = get_transaction_from_kwargs(**kwargs)
    extra_context['transaction'] = transaction

    # Redirect to edit if open
    if not transaction.closed:
        return redirect('transaction_edit', transaction_code=transaction.code)

    # Get print signal, will autoprint with js if true
    print_transaction = request.GET.get('print', False)
    extra_context['print_transaction'] = print_transaction
    return render(request, 'transactions/transaction_detail.html', extra_context)


@login_required
def transaction_document(request, *args, **kwargs):
    extra_context = {}

    # Get the transaction
    transaction = get_transaction_from_kwargs(**kwargs)
    extra_context['transaction'] = transaction

    # Return
    return render(request, 'transactions/transaction_document.html', extra_context)


@login_required
def transaction_edit(request, *args, **kwargs):
    extra_context = {}

    # Get the transaction
    transaction_code = kwargs.get('transaction_code', None)
    if not transaction_code:
        transaction = Transaction.objects.create(employee=request.user)
        return redirect('transaction_edit', transaction_code=transaction.code)

    transaction = get_object_or_404(Transaction, code=transaction_code)
    extra_context['transaction'] = transaction

    # Check that the transaction is open
    if transaction.closed:
        extra_context['message'] = gettext('Transaction Closed')
        return render(request, 'core/message.html', extra_context)

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

            # Clear session data related to this transaction
            clear_transaction_session_data(request.session, transaction)

            # Delete
            transaction.delete()
            return redirect('index')

        # If valid
        if valid:

            # Save the transaction
            transaction.save()

            # Finish later
            if form.cleaned_data['save_button']:
                return redirect('transaction_row', transaction_code=transaction.code)

            # Proceed to pay
            return redirect('transaction_pay', transaction_code=transaction.code)

        else:  # pragma: no cover
            extra_context['form'] = form
            return render(request, 'transactions/transaction_edit.html', extra_context)

    # GET
    else:

        # Create the form
        form = TransactionEditForm(instance=transaction)
        extra_context['form'] = form
        return render(request, 'transactions/transaction_edit.html', extra_context)


@method_decorator(login_required, name='dispatch')
class TransactionList(PaginationMixin, ListView):

    model = Transaction
    context_object_name = 'transactions'
    paginate_by = 8
    # ListView.as_view will pass custom arguments here
    queryset = None
    header = gettext('Transactions')
    request = None
    filter = None
    filter_data = None
    is_filtered = False

    def get(self, request, *args, **kwargs):
        # First

        # Get arguments
        self.request = request
        self.filter_data = kwargs.pop('filter_data', {})

        # Call super
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Third

        # Call the base implementation first
        context = super().get_context_data(**kwargs)

        # Add data
        context['header'] = self.header
        context['filter'] = self.filter
        context['is_filtered'] = self.is_filtered

        return context

    def get_queryset(self):
        # Second

        # Create filter querydict
        data = QueryDict('', mutable=True)
        # Add filters passed from view
        data.update(self.filter_data)
        # Add filters selected by user
        data.update(self.request.GET)

        # Record as filtered
        self.is_filtered = False
        if len([k for k in data.keys() if k != 'page']) > 0:
            self.is_filtered = True

        # Add filters by permission

        # Filter the queryset
        self.filter = TransactionFilter(data)
        self.queryset = self.filter.qs.select_related('cashclose')\
            .prefetch_related('concepts__value__currency') \
            .order_by('-id')  # 79q 27ms

        # Return
        return self.queryset


@login_required
def transaction_pay(request, *args, **kwargs):
    extra_context = {}

    # Get the transaction
    transaction = get_transaction_from_kwargs(**kwargs)
    extra_context['transaction'] = transaction

    # Check that the transaction is open
    if transaction.closed:
        extra_context['message'] = gettext('Transaction Closed')
        return render(request, 'core/message.html', extra_context)

    # Get required payment fields

    # POST
    if request.method == 'POST':
        form = TransactionPayForm(request.POST, instance=transaction)
        valid = form.is_valid()

        # If cancel has been set, delete and go home
        # Note that value is still string before validating
        if form.data['cancel_button'] == 'True':

            # Clear session data related to this transaction
            clear_transaction_session_data(request.session, transaction)

            # Delete
            transaction.delete()
            return redirect('index')

        # If valid
        if valid:

            # Close the transaction
            if form.cleaned_data['confirm_button']:
                transaction.closed = True
                transaction.closed_date = timezone.datetime.now()
                transaction.save()

                # Display and print
                params = urllib.parse.urlencode({'print': True})
                response = redirect('transaction_detail', transaction_code=transaction.code)
                response['Location'] += '?{}'.format(params)
                return response

            # Save the transaction
            if form.cleaned_data['save_button']:
                transaction.save()
                return redirect('transaction_row', transaction_code=transaction.code)

        else:
            extra_context['form'] = form
            return render(request, 'transactions/transaction_pay.html', extra_context)

    # GET
    else:

        # Create the form
        form = TransactionPayForm(instance=transaction)
        extra_context['form'] = form
        return render(request, 'transactions/transaction_pay.html', extra_context)


@login_required()
def transactions_open(request, *args, **kwargs):

    # Set initial filter data
    filter_data = {
        'closed': False,
    }
    params = urllib.parse.urlencode(filter_data)
    # Return
    response = redirect('transaction_list')
    response['Location'] += '?{}'.format(params)
    return response


@login_required
def transaction_row(request, *args, **kwargs):

    # Get the transaction
    transaction = get_transaction_from_kwargs(**kwargs)

    # Set initial filter data
    filter_data = {
        'code': transaction.code,
    }
    params = urllib.parse.urlencode(filter_data)
    # Return
    response = redirect('transaction_list')
    response['Location'] += '?{}'.format(params)
    return response
