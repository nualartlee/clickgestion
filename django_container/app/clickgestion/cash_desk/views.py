from clickgestion.cash_desk.forms import CashCloseForm
from clickgestion.cash_desk.models import get_breakdown_by_concept_type, get_value_totals
from clickgestion.transactions.models import Transaction
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.utils.translation import gettext, gettext_lazy
from django.contrib.auth.decorators import login_required


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
def cash_close(request, *args, **kwargs):
    extra_context = {}

    # Get open transactions
    open_transactions = Transaction.objects.filter(closed=False, cashclose=None)
    extra_context['open_transactions'] = open_transactions

    # Get closed transactions
    closed_transactions = Transaction.objects.filter(closed=True, cashclose=None)
    extra_context['closed_transactions'] = closed_transactions

    # Get breakdown by concept type
    breakdown = get_breakdown_by_concept_type(closed_transactions)
    extra_context['breakdown'] = breakdown

    # Get the totals
    values = []
    for transaction in closed_transactions:
        values += transaction.totals
    totals = get_value_totals(values)
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

        return render(request, 'transactions/cash_close.html', extra_context)


    form = CashCloseForm()
    extra_context['form'] = form
    return render(request, 'transactions/cash_close.html', extra_context)

