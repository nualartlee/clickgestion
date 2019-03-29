from clickgestion.concepts.models import BaseConcept
from clickgestion.cash_desk.filters import CashCloseFilter
from clickgestion.cash_desk.forms import CashCloseForm
from clickgestion.cash_desk.models import CashClose
from clickgestion.core.utilities import custom_permission_required
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.translation import gettext, gettext_lazy
from django.http import QueryDict
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from pure_pagination.mixins import PaginationMixin
from django.utils import timezone
from clickgestion.concepts import totalizers
from clickgestion.transactions.models import Transaction
import urllib


@login_required()
def cash_desk_balance(request, *args, **kwargs):
    extra_context = {}

    # Set the header
    extra_context['document_header'] = gettext('Cash Desk Balance')

    # Create a dummy cashclose to use the same templates
    cashclose = {}
    cashclose['employee'] = {'get_full_name': request.user.get_full_name() }
    cashclose['created'] = timezone.now()

    # Get closed transactions
    closed_transactions = Transaction.objects.filter(closed=True, cashclose=None) \
        .prefetch_related('concepts__value__currency')
    cashclose['transactions'] = closed_transactions

    # Get closed concepts
    closed_concepts = BaseConcept.objects.filter(transaction__in=closed_transactions)\
        .prefetch_related('value__currency')
    cashclose['concepts'] = closed_concepts

    # Get the balance
    balance = totalizers.get_value_totals(closed_concepts)
    cashclose['balance'] = balance

    # Get breakdowns
    breakdowns = [
        totalizers.get_deposits_in_holding_breakdown(),
        totalizers.get_breakdown_by_accounting_group(concepts=closed_concepts),
        totalizers.get_breakdown_by_concept_type(concepts=closed_concepts),
    ]

    # Collect the breakdowns
    cashclose['breakdowns'] = breakdowns

    # Pass the dummy cashclose
    extra_context['cashclose'] = cashclose

    # Render
    return render(request, 'cash_desk/cashclose_detail.html', extra_context)


@custom_permission_required('cash_desk.add_cashclose')
def cash_desk_close(request, *args, **kwargs):
    extra_context = {}

    # Set the header
    extra_context['document_header'] = gettext('Cash Desk Balance')

    # Get closed transactions
    closed_transactions = Transaction.objects.filter(closed=True, cashclose=None) \
        .prefetch_related('concepts__value__currency')
    extra_context['closed_transactions'] = closed_transactions

    # Get closed concepts
    closed_concepts = BaseConcept.objects.filter(transaction__in=closed_transactions) \
        .prefetch_related('value__currency')

    # Get breakdown by concept type
    breakdown = totalizers.get_breakdown_by_concept_type(closed_concepts)
    extra_context['breakdown'] = breakdown

    # Get deposits in holding
    deposits = totalizers.get_deposits_in_holding()
    extra_context['deposits'] = deposits

    # Get the totals
    totals = totalizers.get_value_totals(closed_concepts)
    extra_context['totals'] = totals

    # POST
    if request.method == 'POST':
        form = CashCloseForm(request.POST)
        if form.is_valid():
            cashclose = form.instance
            cashclose.employee = request.user
            cashclose.save()
            # Save cashclose on all transactions
            for transaction in closed_transactions:
                transaction.cashclose = cashclose
                transaction.save()
            # Forward the cash float with deposits

            # Message
            return render(request, 'core/message.html', {'message': gettext('Cash Desk Closed')})

        return render(request, 'cash_desk/cash_desk_close.html', extra_context)  # pragma: no cover

    form = CashCloseForm()
    extra_context['form'] = form
    return render(request, 'cash_desk/cash_desk_close.html', extra_context)


@custom_permission_required('cash_desk.add_cashclose')
def cashclose_detail(request, *args, **kwargs):
    extra_context = {}

    # Set the header
    extra_context['document_header'] = gettext('Cash Desk Close')

    # Get the cashclose
    cashclose_code = kwargs.get('cashclose_code', None)
    cashclose = get_object_or_404(CashClose, code=cashclose_code)
    extra_context['cashclose'] = cashclose

    ## Get closed transactions
    #closed_transactions = Transaction.objects.filter(cashclose=cashclose) \
    #    .prefetch_related('concepts__value__currency')
    #extra_context['closed_transactions'] = closed_transactions

    ## Get closed concepts
    #closed_concepts = BaseConcept.objects.filter(transaction__in=closed_transactions) \
    #    .prefetch_related('value__currency')

    ## Get breakdown by concept type
    #breakdown = totalizers.get_breakdown_by_concept_type(closed_concepts)
    #extra_context['breakdown'] = breakdown

    ## Get deposits in holding
    #deposits = totalizers.get_deposits_in_holding()
    #extra_context['deposits'] = deposits

    ## Get the totals
    #totals = totalizers.get_value_totals(closed_concepts)
    #extra_context['totals'] = totals

    return render(request, 'cash_desk/cashclose_detail.html', extra_context)


@custom_permission_required('cash_desk.add_cashclose')
def cashclose_document(request, *args, **kwargs):
    extra_context = {}

    # Get the cashclose
    cashclose_code = kwargs.get('cashclose_code', None)
    cashclose = get_object_or_404(CashClose, code=cashclose_code)
    extra_context['cashclose'] = cashclose

    # Return
    return render(request, 'cash_desk/cashclose_document.html', extra_context)


@custom_permission_required('cash_desk.add_cashclose')
def cashclose_row(request, *args, **kwargs):

    # Get the cashclose
    cashclose_code = kwargs.get('cashclose_code', None)
    cashclose = get_object_or_404(CashClose, code=cashclose_code)

    # Set initial filter data
    filter_data = {
        'code': cashclose.code,
    }
    params = urllib.parse.urlencode(filter_data)
    # Return
    response = redirect('cashclose_list')
    response['Location'] += '?{}'.format(params)
    return response


@method_decorator(custom_permission_required('cash_desk.add_cashclose'), name='dispatch')
class CashCloseList(PaginationMixin, ListView):

    model = CashClose
    context_object_name = 'cashcloses'
    paginate_by = 8
    # ListView.as_view will pass custom arguments here
    queryset = None
    header = gettext_lazy('Cash Desk Closures')
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
        self.filter = CashCloseFilter(data)
        self.queryset = self.filter.qs \
            .prefetch_related('transactions__concepts__value__currency') \
            .order_by('-id')  # 79q 27ms

        # Return
        return self.queryset

