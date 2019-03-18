from django.apps import apps
from django.utils.decorators import available_attrs
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, reverse
from functools import wraps


def invalid_permission_redirect(request):
    """
    Return a login or a permission denied if already logged in.

    :param request:
    :return:
    """
    if request.user.is_authenticated:
        raise PermissionDenied()
    else:
        return redirect(
            reverse('login'),
            extra_context={'next': request.path},
        )


def custom_permission_required(permission):
    """
    Decorator for views that checks that the user has the given permission,
    redirecting to the log-in page or permission denied as necessary.
    :param permission: Permission id in 'app.permission' format.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect(
                    reverse('login'),
                    extra_context={'next': request.path},
                )
            if request.user.has_perm(permission):
                return view_func(request, *args, **kwargs)
            raise PermissionDenied()
        return _wrapped_view
    return decorator
