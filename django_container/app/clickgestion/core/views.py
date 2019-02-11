from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from clickgestion.core.forms import CoreAuthenticationForm

@login_required()
def index(request):
    return render(request, 'core/index.html')


def login(request):
    return auth_views.login(
        request,
        template_name='core/login.html',
        authentication_form=CoreAuthenticationForm,
    )