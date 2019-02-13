from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, reverse


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
