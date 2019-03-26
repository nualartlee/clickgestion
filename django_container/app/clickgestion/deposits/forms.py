from clickgestion.deposits.models import AptRentalDeposit, DepositReturn
from crispy_forms.layout import Column, Field, HTML, Row
from clickgestion.concepts.forms import ConceptForm
from django.forms import DateField, DateInput
from crispy_forms.helper import FormHelper, Layout
from django.utils.translation import gettext_lazy


class AptRentalDepositForm(ConceptForm):
    start_date = DateField(
        widget=DateInput(
            attrs={'type': 'date'},
        ),
    )
    end_date = DateField(
        widget=DateInput(
            attrs={'type': 'date'},
        ),
    )

    class Meta:
        model = AptRentalDeposit
        fields = ('adults', 'children', 'end_date', 'start_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    Field(
                        'start_date',
                        title=gettext_lazy("Arrival date"),
                        css_class='col-8',
                    ),
                    css_class='col-6',
                ),
                Column(
                    Field(
                        'end_date',
                        title=gettext_lazy("Departure date"),
                        css_class='col-8',
                    ),
                    css_class='col-6',
                ),
            ),
            Row(
                Column(
                    Field(
                        'adults',
                        title=gettext_lazy("Number of adults"),
                        css_class='col-8',
                    ),
                    css_class='col-6',
                ),
                Column(
                    Field(
                        'children',
                        title=gettext_lazy("Number of children"),
                        css_class='col-8',
                    ),
                    css_class='col-6',
                ),
            ),
        )


class DepositReturnForm(ConceptForm):

    class Meta:
        model = DepositReturn
        fields = ('returned_deposit',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                Column(
                    HTML('<p>{{ concept.description_short }}</p>'),
                    css_class='col',
                ),
            ),
        )
