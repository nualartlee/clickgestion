from django.apps import apps
from clickgestion.concepts.models import BaseConcept
from django.shortcuts import get_object_or_404, render, redirect, reverse
from clickgestion.transactions.views import get_transaction_from_kwargs
from django.utils.translation import gettext, gettext_lazy
from clickgestion.concepts.filters import ConceptFilter
from django.views.generic import ListView
from clickgestion.core.views import message
from django.contrib.auth.decorators import login_required
from pure_pagination.mixins import PaginationMixin
from django.http import QueryDict
import urllib
from django.utils.decorators import method_decorator


@login_required
def concept_actions(request, *args, **kwargs):  # pragma: no cover
    extra_context = {}

    # Get the concept
    concept_code = kwargs.get('concept_code', None)
    concept = get_object_or_404(BaseConcept, code=concept_code)
    extra_context['concept'] = concept

    # Return
    return render(request, 'concepts/concept_actions.html', extra_context)


def concept_delete(request, *args, **kwargs):  # pragma: no cover
    extra_context = {}

    # Get the concept and form
    concept, concept_form = get_concept_and_form_from_kwargs(**kwargs)
    extra_context['concept'] = concept

    # Get the transaction
    transaction = concept.transaction
    if transaction.closed:
        return redirect('message', message=gettext('Transaction Closed'))
    extra_context['transaction'] = transaction

    # Use default delete view
    extra_context['header'] = gettext('Delete {}?'.format(concept.name))
    extra_context['message'] = concept.description_short
    extra_context['next'] = request.META['HTTP_REFERER']

    # POST
    if request.method == 'POST':
        default_next = reverse('transaction_detail', kwargs={'transaction_code': concept.transaction.code})
        concept.delete()
        next_page = request.POST.get('next', default_next)
        return redirect(next_page)

    # GET
    else:
        return render(request, 'core/delete.html', extra_context)


def concept_detail(request, *args, **kwargs):  # pragma: no cover
    extra_context = {}

    # Check permissions

    # Get the concept and form
    concept, concept_form = get_concept_and_form_from_kwargs(**kwargs)
    extra_context['concept'] = concept
    form = concept_form(instance=concept)
    extra_context['form'] = form

    # Get the transaction
    transaction = concept.transaction
    extra_context['transaction'] = transaction

    return render(request, 'concepts/concept_detail.html', extra_context)


def concept_edit(request, *args, **kwargs):  # pragma: no cover
    extra_context = {}

    # Check permissions

    # Get the concept and form
    concept, concept_form = get_concept_and_form_from_kwargs(**kwargs)
    extra_context['concept'] = concept

    # Get the transaction
    transaction = concept.transaction
    if transaction.closed:
        extra_context['message'] = gettext('Transaction Closed')
        return message(request, extra_context)
    extra_context['transaction'] = transaction

    # POST
    if request.method == 'POST':
        form = concept_form(request.POST, instance=concept)
        if form.is_valid():
            form.save()
            return redirect('transaction_edit', transaction_code=transaction.code)

        else:
            extra_context['form'] = form
            return render(request, 'concepts/concept_edit.html', extra_context)

    # GET
    else:

        # Get the form
        form = concept_form(instance=concept)
        extra_context['form'] = form
        return render(request, 'concepts/concept_edit.html', extra_context)


@method_decorator(login_required, name='dispatch')
class ConceptList(PaginationMixin, ListView):

    template_name = 'concepts/concept_list.html'
    model = BaseConcept
    context_object_name = 'concepts'
    paginate_by = 8
    # ListView.as_view will pass custom arguments here
    queryset = None
    header = gettext_lazy('Concepts')
    request = None
    filter_type = ConceptFilter
    filter = None
    filter_data = None
    is_filtered = False

    def get(self, request, *args, **kwargs):
        # First

        # Get arguments
        self.request = request
        self.filter_data = kwargs.pop('filter_data', {})

        # Call super
        return super().get(self, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        # Third

        # Call the base implementation first
        context = super().get_context_data(**kwargs)

        # Add data
        context['header'] = self.header
        context['filter'] = self.filter
        context['is_filtered'] = self.is_filtered

        return context

    def get_queryset(self):
        # Second

        # Create filter querydict
        data = QueryDict('', mutable=True)
        # Add filters passed from view
        data.update(self.filter_data)
        # Add filters selected by user
        data.update(self.request.GET)

        # Record as filtered
        self.is_filtered = False
        if len([k for k in data.keys() if k != 'page']) > 0:
            self.is_filtered = True

        # Add filters by permission

        # Filter the queryset
        self.filter = self.filter_type(data)
        self.queryset = self.filter.qs.select_related('transaction') \
            .prefetch_related('value__currency') \
            .order_by('-id')  # 79q 27ms

        # Return
        return self.queryset


@login_required()
def concept_refund(request, *args, **kwargs):  # pragma: no cover
    extra_context = {}

    # Check permissions

    # Get the concept and form
    concept, concept_form = get_concept_and_form_from_kwargs(**kwargs)
    extra_context['concept'] = concept

    # Get the transaction
    transaction = concept.transaction
    extra_context['transaction'] = transaction

    return render(request, 'concepts/concept_detail.html', extra_context)


@login_required()
def concept_row(request, *args, **kwargs):  # pragma: no cover

    # Get the concept
    concept_code = kwargs.get('concept_code', None)
    concept = get_object_or_404(BaseConcept, code=concept_code)

    # Set initial filter data
    filter_data = {
        'code': concept.code,
    }
    params = urllib.parse.urlencode(filter_data)
    # Return
    response = redirect('concept_list')
    response['Location'] += '?{}'.format(params)
    return response


def get_concept_and_form_from_kwargs(**kwargs):

    # Get the form
    concept_form = kwargs.get('concept_form', None)

    # Get the concept class
    concept_class = concept_form._meta.model

    # If a transaction code is provided, this is a new concept
    transaction_code = kwargs.get('transaction_code', None)
    if transaction_code:
        transaction = get_transaction_from_kwargs(**kwargs)
        return concept_class(transaction=transaction), concept_form

    # Get the existing concept
    concept_code = kwargs.get('concept_code', None)
    concept = get_object_or_404(concept_class, code=concept_code)
    return concept, concept_form


