from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from clickgestion.core.forms import CoreAuthenticationForm


def badrequest(request, exception):  # pragma: no cover
    response = render(request, 'core/400.html')
    response.status_code = 400
    return response


@login_required()
def index(request):
    return render(request, 'core/index.html')


def login(request):
    return auth_views.login(
        request,
        template_name='core/login.html',
        authentication_form=CoreAuthenticationForm,
    )


def forbidden(request, exception):
    """
    Returned when a django.core.exceptions.PermisionDenied is raised.

    :param request:
    :param exception:
    :return:
    """
    response = render(request, 'core/403.html')
    response.status_code = 403
    return response


def message(request):
    return render(request, 'core/message.html')


def notfound(request, exception):
    """
    Returned for failed get_object_or_404 calls.

    :param request:
    :param exception:
    :return:
    """
    response = render(request, 'core/404.html')
    response.status_code = 404
    return response


def servererror(request):  # pragma: no cover
    """
    Returned for unhandled exceptions in views.

    :param request:
    :param exception:
    :return:
    """
    response = render(request, 'core/500.html')
    response.status_code = 500
    return response


