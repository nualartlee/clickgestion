from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from clickgestion.transactions.models import Transaction
from clickgestion.transactions.forms import TransactionForm


@login_required()
def new_transaction(request):
    extra_context = {}

    if request.method == 'POST':

        return redirect('login')

    else:
        transaction_form = TransactionForm()
        extra_context['transaction_form'] = transaction_form
        return render(request, 'transactions/new_transaction.html', extra_context)


