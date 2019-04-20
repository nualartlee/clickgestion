from django.apps import apps
from django import forms
from django.utils.translation import gettext_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column
from clickgestion.apt_rentals.models import AptRental
from clickgestion.concepts.forms import ConceptForm
from django.utils import timezone
from django.core.exceptions import ValidationError


class AptRentalForm(ConceptForm):
    add_deposit = forms.BooleanField(
        label=gettext_lazy('Add Deposit'),
        initial=False,
        required=False,
    )
    #end_date = forms.DateField(
    #    format='%Y-%m-%d',
    #    label=gettext_lazy('Departure Date'),
    #    widget=forms.DateInput(
    #        attrs={'type': 'date'},
    #    ),
    #)
    #start_date = forms.DateField(
    #    format='%Y-%m-%d',
    #    label=gettext_lazy('Arrival Date'),
    #    widget=forms.DateInput(
    #        attrs={'type': 'date'},
    #    ),
    #)

    class Meta:
        model = AptRental
        fields = ('adults', 'children', 'end_date', 'start_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.set_layout()

    def set_layout(self):
        self.fields['end_date'].label = gettext_lazy('Departure Date')
        self.fields['start_date'].label = gettext_lazy('Arrival Date')
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
            Row(
                Column(
                    Field(
                        'add_deposit',
                        title=gettext_lazy("Add Apartment Deposit"),
                        css_class='col-8',
                    ),
                    css_class='col-6',
                ),
            ),
        )

    def clean(self):

        # Assert that all nightly prices are set
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if not start_date or not end_date:
            return
        rates = AptRental(
            start_date=start_date,
            end_date=end_date,
        ).get_current_rates()
        if 'missing' in rates:
            error = gettext_lazy('Missing prices in selected dates.')
            raise ValidationError(error)

        # Assert that departure is after arrival
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if start_date and end_date:
            if start_date == end_date:
                error = gettext_lazy('Departure date is the same as arrival.')
                raise ValidationError(error)
            if start_date > end_date:
                error = gettext_lazy('Departure date is before arrival.')
                raise ValidationError(error)

        # Assert number of people
        adults = self.cleaned_data.get('adults')
        children = self.cleaned_data.get('children')
        if adults and children:
            if adults + children > 5:
                error = gettext_lazy('Five people maximum.')
                raise ValidationError(error)

        return self.cleaned_data

    def clean_adults(self):
        adults = self.cleaned_data.get('adults')
        if adults > 4 or adults < 1:
            error = gettext_lazy('One to four adults only.')
            raise ValidationError(error)
        return adults

    def clean_children(self):
        children = self.cleaned_data.get('children')
        if children > 4 or children < 0:
            error = gettext_lazy('Up to four children only.')
            raise ValidationError(error)
        return children

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if start_date < (timezone.now() - timezone.timedelta(days=30)).date():
            error = gettext_lazy('Arrival date is too far back.')
            raise ValidationError(error)
        return start_date

    def save(self, commit=True):
        aptrental = super().save(commit=False)
        if commit:
            aptrental.save()
            if self.cleaned_data['add_deposit']:
                deposit = apps.get_model('deposits.AptRentalDeposit')(aptrental=aptrental)
                deposit.save()
        return aptrental
