from django import template

register = template.Library()


@register.simple_tag
def update_query_params(request, **kwargs):
    """
    Update the current url query parameters with the given.

    :param request: The current request
    :param kwargs: The parameters, e.g.: a=1.
    :return: The parameter string to be appended to the url.
    """
    updated = request.GET.copy()
    updated.update(kwargs)
    # django update() keeps previous values of a key in a list
    purged = dict(updated.items())
    updated.clear()
    updated.update(purged)
    return updated.urlencode()
