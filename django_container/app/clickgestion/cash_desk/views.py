from clickgestion.cash_desk.forms import CashCloseForm
from clickgestion.cash_desk.models import CashClose
from clickgestion.transactions.models import BaseConcept, Transaction
from clickgestion.transactions import totalizers
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.utils.translation import gettext, gettext_lazy
from django.contrib.auth.decorators import login_required
from django.utils import timezone


@login_required()
def cash_desk_balance(request, *args, **kwargs):
    extra_context = {}
    # 268q 72ms
    # 236q 59ms
    # 115q 36ms

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
    return render(request, 'cash_desk/cash_desk_balance.html', extra_context)


def cashclose_detail(request, *args, **kwargs):
    extra_context = {}

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

    # Get the totals
    totals = totalizers.get_value_totals(closed_concepts)
    extra_context['totals'] = totals

    return render(request, 'cash_desk/cashclose_detail.html', extra_context)


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

