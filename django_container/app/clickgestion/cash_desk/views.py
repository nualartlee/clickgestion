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

    # Get closed transactions
    transactions = Transaction.objects.filter(closed=True, cashclose=None).prefetch_related('concepts__value__currency')
    extra_context['transactions'] = transactions

    concepts = BaseConcept.objects.filter(transaction__closed=True, transaction__cashclose=None).prefetch_related('value__currency')
    # Get breakdown by concept type
    #breakdown = totalizers.get_breakdown_by_concept_type(transactions)
    breakdown = totalizers.get_breakdown_by_concept_type(concepts)
    extra_context['breakdown'] = breakdown

    # Get the totals
    values = []
    for transaction in transactions:
        values += transaction.totals
    totals = totalizers.get_value_totals(values)
    extra_context['totals'] = totals

    # Get deposits in holding
    date = timezone.now() - timezone.timedelta(days=90)
    transactions = Transaction.objects.filter(closed_date__date__gte=date)
    deposits = totalizers.get_deposits_in_holding(transactions)
    extra_context['deposits'] = deposits

    # Render
    return render(request, 'cash_desk/cash_desk_balance.html', extra_context)


def cashclose_detail(request, *args, **kwargs):
    extra_context = {}

    # Get the cashclose
    cashclose_code = kwargs.get('cashclose_code', None)
    cashclose = get_object_or_404(CashClose, code=cashclose_code)
    extra_context['cashclose'] = cashclose

    # Get the totals
    values = []
    for transaction in cashclose.transactions.all():
        values += transaction.totals
    totals = totalizers.get_value_totals(values)
    extra_context['totals'] = totals

    # Get breakdown by concept type
    breakdown = totalizers.get_breakdown_by_concept_type(cashclose.transactions.all())
    extra_context['breakdown'] = breakdown

    return render(request, 'cash_desk/cashclose_detail.html', extra_context)


@login_required()
def cash_desk_close(request, *args, **kwargs):
    extra_context = {}

    # Get open transactions
    open_transactions = Transaction.objects.filter(closed=False, cashclose=None)
    extra_context['open_transactions'] = open_transactions

    # Get closed transactions
    closed_transactions = Transaction.objects.filter(closed=True, cashclose=None)
    extra_context['closed_transactions'] = closed_transactions

    # Get breakdown by concept type
    breakdown = totalizers.get_breakdown_by_concept_type(closed_transactions)
    extra_context['breakdown'] = breakdown

    # Get the totals
    values = []
    for transaction in closed_transactions:
        values += transaction.totals
    totals = totalizers.get_value_totals(values)
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

