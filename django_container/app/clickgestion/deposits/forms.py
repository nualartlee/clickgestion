from clickgestion.deposits.models import AptRentalDeposit, DepositReturn, ParkingRentalDeposit
from crispy_forms.layout import Column, HTML, Row
from clickgestion.apt_rentals.forms import AptRentalForm
from clickgestion.concepts.forms import ConceptForm
from django.forms import HiddenInput
from crispy_forms.helper import FormHelper, Layout


class AptRentalDepositForm(AptRentalForm):

    class Meta:
        model = AptRentalDeposit
        fields = ('adults', 'children', 'end_date', 'start_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_deposit = self.fields['add_deposit']
        add_deposit.initial = False
        add_deposit.widget = HiddenInput()


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


class ParkingRentalDepositForm(AptRentalForm):

    class Meta:
        model = ParkingRentalDeposit
        fields = ('end_date', 'start_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_deposit = self.fields['add_deposit']
        add_deposit.initial = False
        add_deposit.widget = HiddenInput()
