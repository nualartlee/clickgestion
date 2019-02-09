from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from clickgestion.main.models import Transaction


@login_required()
def index(request):
    return render(request, 'main/index.html')

@login_required()
def transaction(request):
    new_transaction = Transaction()


