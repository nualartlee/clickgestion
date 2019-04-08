from crispy_forms.bootstrap import AppendedText, PrependedAppendedText, PrependedText
from django.apps import apps
from django import forms
from django.utils.translation import gettext_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column
from clickgestion.ticket_sales.models import TicketSale
from clickgestion.concepts.forms import ConceptForm
from django.utils import timezone
from django.core.exceptions import ValidationError


class TicketSalesForm(ConceptForm):
    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'},
        ),
    )
    price_per_adult = forms.FloatField(min_value=0, disabled=True, required=False)
    price_per_child = forms.FloatField(min_value=0, disabled=True, required=False)
    price_per_senior = forms.FloatField(min_value=0, disabled=True, required=False)
    show = forms.ModelChoiceField(
        queryset=apps.get_model('ticket_sales.show').objects.filter(enabled=True),
        initial=apps.get_model('ticket_sales.show').objects.filter(enabled=True).first(),
    )
    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'},
        ),
    )

    class Meta:
        model = TicketSale
        fields = ('adults', 'children', 'end_date', 'seniors', 'show', 'start_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Get the selected show
        show_id = self.data.get('show', False)
        if show_id:
            self.show = apps.get_model('ticket_sales.show').objects.get(id=show_id)
        else:
            self.show = self.fields['show'].initial

        # Set form
        self.set_required_fields()
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('final_submit'),
            Row(
                Column(
                    Field(
                        'show',
                        title=gettext_lazy("Tour/Show"),
                        css_class='col-12',
                        onchange='document.getElementById("id_final_submit").value="False";form.submit();',
                    ),
                    css_class='col-6',
                ),
            ),
            Row(
                Column(
                    Field(
                        'start_date',
                        title=gettext_lazy("Tour/Show date"),
                        css_class='col-8',
                    ),
                    css_class='col-6',
                ),
                Column(
                    Field(
                        'end_date',
                        title=gettext_lazy("End date"),
                        css_class='col-8',
                    ),
                    css_class='col-6',
                ),
            ),
            Row(
                Column(
                    Field(
                        'adults',
                        title=gettext_lazy('Number of adults') if self.show.per_adult
                        else gettext_lazy('Number of units'),
                        css_class='col-auto',
                    ),
                    AppendedText(
                        'price_per_adult',
                        self.show.currency.symbol,
                        title=gettext_lazy('Price per adult') if self.show.per_adult else
                        gettext_lazy('Price per unit') if self.show.per_unit else
                        gettext_lazy('Price'),
                        css_class='col-auto',
                        value=self.show.price_per_adult,
                    ),
                    css_class='col-2',
                ),
                Column(
                    Field(
                        'children',
                        title=gettext_lazy('Number of children'),
                        css_class='col-auto',
                    ),
                    AppendedText(
                        'price_per_child',
                        self.show.currency.symbol,
                        title=gettext_lazy('Price per child'),
                        css_class='col-auto',
                        value=self.show.price_per_child,
                    ),
                    css_class='col-2',
                ),
                Column(
                    Field(
                        'seniors',
                        title=gettext_lazy('Number of seniors'),
                        css_class='col-auto',
                    ),
                    AppendedText(
                        'price_per_senior',
                        self.show.currency.symbol,
                        title=gettext_lazy('Price per senior'),
                        css_class='col-auto',
                        value=self.show.price_per_senior,
                    ),
                    css_class='col-2',
                ),
            ),
        )

    def clean(self):

        # Assert that start date is before end
        start_date = self.cleaned_data.get('start_date')
        end_date = self.cleaned_data.get('end_date')
        if start_date and end_date:
            if self.show.per_night:
                if start_date > end_date:
                    error = gettext_lazy('End date is before start.')
                    raise ValidationError(error)

        # Assert number
        adults = self.cleaned_data.get('adults', 0)
        children = self.cleaned_data.get('children', 0)
        seniors = self.cleaned_data.get('seniors', 0)
        if not self.show.per_unit:
            if adults + children + seniors <= 0:
                error = gettext_lazy('No people')
                raise ValidationError(error)

        return self.cleaned_data

    def clean_adults(self):
        adults = self.cleaned_data.get('adults')
        if self.show.per_unit:
            minimum = 1
        else:
            minimum = 0
        if adults < minimum:
            error = gettext_lazy('Invalid value')
            raise ValidationError(error)
        return adults

    def clean_children(self):
        children = self.cleaned_data.get('children')
        if children < 0:
            error = gettext_lazy('Invalid value')
            raise ValidationError(error)
        return children

    def clean_seniors(self):
        seniors = self.cleaned_data.get('seniors')
        if seniors < 0:
            error = gettext_lazy('Invalid value')
            raise ValidationError(error)
        return seniors

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if self.fields['start_date'].required:
            if start_date < (timezone.now() - timezone.timedelta(days=30)).date():
                error = gettext_lazy('Ticket date is too far back.')
                raise ValidationError(error)
        return start_date

    def save(self, commit=True):
        ticketsale = super().save(commit=False)
        if self.show.variable_price:
            ticketsale.show.price_per_adult = self.cleaned_data['price_per_adult']
            ticketsale.show.price_per_child = self.cleaned_data['price_per_child']
            ticketsale.show.price_per_senior = self.cleaned_data['price_per_senior']
        if commit:
            ticketsale.save()
        return ticketsale

    def set_required_fields(self, *args, **kwargs):
        """
        Sets which form fields are required according to the show
        """

        # Start date
        if not (self.show.date_required or self.show.per_night):
            self.fields['start_date'].widget = forms.HiddenInput()
            self.fields['start_date'].required = False

        # End date
        if not self.show.per_night:
            self.fields['end_date'].widget = forms.HiddenInput()
            self.fields['end_date'].required = False

        # Adults
        if self.show.per_transaction:
            self.fields['adults'].widget = forms.HiddenInput()
            self.fields['adults'].required = False
        if self.show.per_unit:
            self.fields['adults'].label = gettext_lazy('Units')
        if self.show.per_adult:
            self.fields['adults'].label = gettext_lazy('Adults')
        if self.show.variable_price:
            self.fields['price_per_adult'].disabled = False
        self.fields['price_per_adult'].label = ''

        # Children
        if self.show.per_child:
            self.fields['price_per_child'].label = ''
            if self.show.variable_price:
                self.fields['price_per_child'].disabled = False
        else:
            self.fields['children'].widget = forms.HiddenInput()
            self.fields['children'].required = False
            self.fields['price_per_child'].widget = forms.HiddenInput()

        # Seniors
        if self.show.per_senior:
            self.fields['price_per_senior'].label = ''
            if self.show.variable_price:
                self.fields['price_per_senior'].disabled = False
        else:
            self.fields['seniors'].widget = forms.HiddenInput()
            self.fields['seniors'].required = False
            self.fields['price_per_senior'].widget = forms.HiddenInput()
