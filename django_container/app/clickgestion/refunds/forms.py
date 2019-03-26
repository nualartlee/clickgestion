from django import forms
from crispy_forms.helper import FormHelper, Layout
from crispy_forms.layout import Column, Row, HTML
from clickgestion.refunds.models import Refund


class RefundForm(forms.ModelForm):

    class Meta:
        model = Refund
        fields = '__all__'

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
