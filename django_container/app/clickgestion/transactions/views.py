from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from clickgestion.transactions.models import Transaction
from clickgestion.transactions.forms import TransactionForm


@login_required()
def new_transaction(request):
    extra_context = {}
    transaction = Transaction()

    if request.method == 'POST':

        return redirect('login')

    else:
        transaction_form = TransactionForm(transaction)
        extra_context['transaction'] = transaction
        extra_context['transaction_form'] = transaction_form
        return render(request, 'core/transaction.html', extra_context)


