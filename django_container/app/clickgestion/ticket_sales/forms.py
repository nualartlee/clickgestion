from crispy_forms.bootstrap import AppendedText
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
    show = forms.ModelChoiceField(
        queryset=apps.get_model('ticket_sales.show').objects.filter(enabled=True),
        initial=apps.get_model('ticket_sales.show').objects.filter(enabled=True).first(),
    )
    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'},
        ),
    )
    end_date = forms.DateField(
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
                    AppendedText(
                        'adults',
                        '{}{}'.format(self.show.currency.symbol, self.show.price_per_adult),
                        title=self.fields['adults'].widget.title,
                        label=self.fields['adults'].label,
                        css_class='col-6',
                    ),
                    css_class='col-2',
                ),
                Column(
                    AppendedText(
                        'children',
                        '{}{}'.format(self.show.currency.symbol, self.show.price_per_child),
                        title=gettext_lazy("Number of children"),
                        css_class='col-6',
                    ),
                    css_class='col-2',
                ),
                Column(
                    AppendedText(
                        'seniors',
                        '{}{}'.format(self.show.currency.symbol, self.show.price_per_senior),
                        title=gettext_lazy("Number of seniors"),
                        css_class='col-6',
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
            if self.instance.show.per_night:
                if start_date > end_date:
                    error = gettext_lazy('End date is before start.')
                    raise ValidationError(error)

        # Assert number of people
        adults = self.cleaned_data.get('adults')
        children = self.cleaned_data.get('children')
        if adults and children:
            if adults + children == 0:
                error = gettext_lazy('No people')
                raise ValidationError(error)

        return self.cleaned_data

    def clean_adults(self):
        adults = self.cleaned_data.get('adults')
        if adults < 0:
            error = gettext_lazy('Invalid value')
            raise ValidationError(error)
        return adults

    def clean_children(self):
        children = self.cleaned_data.get('children')
        if children < 0:
            error = gettext_lazy('Invalid value')
            raise ValidationError(error)
        return children

    def clean_start_date(self):
        start_date = self.cleaned_data.get('start_date')
        if self.fields['start_date'].required:
            if start_date < (timezone.now() - timezone.timedelta(days=30)).date():
                error = gettext_lazy('Ticket date is too far back.')
                raise ValidationError(error)
        return start_date

    def save(self, commit=True):
        ticketsale = super().save(commit=False)
        if commit:
            ticketsale.save()
        return ticketsale

    def set_required_fields(self, *args, **kwargs):
        """
        Sets which form fields are required according to the show
        """

        # Hide start date
        if not (self.show.date_required or self.show.per_night):
            self.fields['start_date'].widget = forms.HiddenInput()
            self.fields['start_date'].required = False
        # Hide end date
        if not self.show.per_night:
            self.fields['end_date'].widget = forms.HiddenInput()
            self.fields['end_date'].required = False
        # Hide adults
        if self.show.per_transaction:
            self.fields['adults'].widget = forms.HiddenInput()
            self.fields['adults'].required = False
        # Set unit label
        if self.show.per_unit:
            self.fields['adults'].label = gettext_lazy('Units')
            self.fields['adults'].widget.title = gettext_lazy('Number of units')
        # Set adult label
        if self.show.per_adult:
            self.fields['adults'].widget.label = gettext_lazy('Adults')
            self.fields['adults'].widget.title = gettext_lazy('Number of adults')
        # Hide children
        if not self.show.per_child:
            self.fields['children'].widget = forms.HiddenInput()
            self.fields['children'].required = False
        # Hide seniors
        if not self.show.per_senior:
            self.fields['seniors'].widget = forms.HiddenInput()
            self.fields['seniors'].required = False
