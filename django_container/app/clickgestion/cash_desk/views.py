from clickgestion.cash_desk.filters import CashCloseFilter
from clickgestion.cash_desk.forms import CashCloseForm
from clickgestion.cash_desk.models import CashClose
from clickgestion.concepts.models import BaseConcept
from clickgestion.transactions.models import Transaction
from django.shortcuts import get_object_or_404, render, redirect
from django.utils.translation import gettext, gettext_lazy
from django_xhtml2pdf.utils import generate_pdf
from django.http import HttpResponse, QueryDict
from clickgestion.core.utilities import invalid_permission_redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from pure_pagination.mixins import PaginationMixin
from clickgestion.concepts import totalizers
import urllib


@login_required()
def cash_desk_balance(request, *args, **kwargs):
    # 268q 72ms
    # 236q 59ms
    # 115q 36ms
    extra_context = {}

    # Set the header
    extra_context['document_header'] = gettext('Cash Desk Balance')

    # Get closed transactions
    closed_transactions = Transaction.objects.filter(closed=True, cashclose=None) \
        .prefetch_related('concepts__value__currency')
    extra_context['closed_transactions'] = closed_transactions

    # Get closed concepts
    closed_concepts = BaseConcept.objects.filter(transaction__in=closed_transactions)\
        .prefetch_related('value__currency')

    # Get breakdown by concept type
    breakdown = totalizers.get_breakdown_by_concept_type(closed_concepts)
    extra_context['breakdown'] = breakdown

    # Get the totals
    totals = totalizers.get_value_totals(closed_concepts)
    extra_context['totals'] = totals

    # Get deposits in holding
    deposits = totalizers.get_deposits_in_holding()
    extra_context['deposits'] = deposits

    # Render
    return render(request, 'cash_desk/cashclose_detail.html', extra_context)


def cashclose_detail(request, *args, **kwargs):
    extra_context = {}

    # Set the header
    extra_context['document_header'] = gettext('Cash Desk Close')

    # Get the cashclose
    cashclose_code = kwargs.get('cashclose_code', None)
    cashclose = get_object_or_404(CashClose, code=cashclose_code)
    extra_context['cashclose'] = cashclose

    # Get closed transactions
    closed_transactions = Transaction.objects.filter(cashclose=cashclose) \
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

    return render(request, 'cash_desk/cashclose_detail.html', extra_context)


@login_required()
def cashclose_row(request, *args, **kwargs):

    # Check permissions
    if not request.user.is_authenticated:
        return invalid_permission_redirect(request)

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

        # Check permissions
        if not request.user.is_authenticated:
            return invalid_permission_redirect(request)

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

    def post(self, request, *args, **kwargs):

        # Check permissions
        if not request.user.is_authenticated:
            return invalid_permission_redirect(request)

        print_cashclose = request.POST.get('print_cashclose', None)
        if print_cashclose:
            # Get the cashclose
            cashclose = get_object_or_404(CashClose, code=print_cashclose)
            # Create an http response
            resp = HttpResponse(content_type='application/pdf')
            resp['Content-Disposition'] = 'attachment; filename="{}.pdf"'.format(cashclose.code)
            # Set context
            context = {
                'cashclose': cashclose,
            }
            # Generate the pdf
            result = generate_pdf('cash_desk/cashclose.html', file_object=resp, context=context)
            return result

        # Return same
        request.method = 'GET'
        return self.get(request, *args, **kwargs)


@login_required()
def cash_desk_close(request, *args, **kwargs):
    extra_context = {}

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

        return render(request, 'cash_desk/cash_desk_close.html', extra_context)


    form = CashCloseForm()
    extra_context['form'] = form
    return render(request, 'cash_desk/cash_desk_close.html', extra_context)

