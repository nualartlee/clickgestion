from clickgestion.concepts.forms import ConceptForm
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Row, HTML
from clickgestion.deposits.models import AptRentalDeposit, DepositReturn


class AptRentalDepositForm(ConceptForm):

    class Meta:
        model = AptRentalDeposit
        fields = ('adults', 'children', 'end_date', 'start_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.layout = Layout(
            Row(
                HTML('<p>{{ concept.description_short }}</p>'),
                css_class='justify-content-center',

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
        self.layout = Layout(
            Row(
                HTML('<p>{{ concept.description_short }}</p>'),
                css_class='justify-content-center',

            ),
        )
