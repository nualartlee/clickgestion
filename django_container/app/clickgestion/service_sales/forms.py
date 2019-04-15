from crispy_forms.bootstrap import AppendedText
from django.apps import apps
import copy
from django import forms
from django.utils.translation import gettext_lazy
from django.forms.fields import FileField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Row, Column
from clickgestion.service_sales.models import ServiceSale
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core.validators import MinValueValidator


class ServiceSalesForm(forms.Form):
    adults = forms.IntegerField(validators=[MinValueValidator(0)])
    children = forms.IntegerField(validators=[MinValueValidator(0)])
    type = forms.ModelChoiceField(
        queryset=apps.get_model('service_sales.ServiceType').objects.none(),
        empty_label=None,
    )
    end_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'},
        ),
    )
    # This flag controls the final submit, set as false to update fields dynamically and reload the form
    final_submit = forms.BooleanField(
        initial=True,
        required=False,
        widget=forms.HiddenInput()
    )
    price_per_adult = forms.DecimalField(min_value=0, disabled=True, required=False)
    price_per_child = forms.DecimalField(min_value=0, disabled=True, required=False)
    price_per_senior = forms.DecimalField(min_value=0, disabled=True, required=False)
    price_per_unit = forms.DecimalField(min_value=0, disabled=True, required=False)
    seniors = forms.IntegerField(validators=[MinValueValidator(0)])
    service = forms.ModelChoiceField(
        queryset=apps.get_model('service_sales.Service').objects.none(),
        empty_label=None,
    )
    start_date = forms.DateField(
        widget=forms.DateInput(
            attrs={'type': 'date'},
        ),
        validators=[MinValueValidator((timezone.now() - timezone.timedelta(days=30)).date())],
    )
    units = forms.IntegerField(validators=[MinValueValidator(1)])

    # Passing this form as a ModelForm to make it compatible with default concept views
    class Meta:
        model = ServiceSale
    _meta = Meta

    def __init__(self, *args, **kwargs):
        self._current_post_data = None
        self.selected_type = None
        self.type_choices = None
        self.selected_service = None
        self.service_choices = None
        self.instance = None
        if kwargs.get('instance', False):
            self.instance = kwargs.pop('instance')
        super().__init__(*args, **kwargs)
        self.set_choices()
        self.set_initial_values()
        self.set_current_values()
        self.set_fields()
        self.set_layout()

    def add_input_data(self, field_name, python_value):
        """
        Adds/replaces stored user input to the form.

        :param field_name: The name of the field to add data to
        :param value: The python value to set (will be converted to be displayed on form)
        """
        data_copy = copy.deepcopy(self.data)
        data_copy[field_name] = self.fields[field_name].prepare_value(python_value)
        self.data = data_copy

    def clean(self):

        # Pass if not final submit
        if not self.cleaned_data.get('final_submit', False):
            return self.cleaned_data

        # Assert that start date is before end
        end_date = self.cleaned_data.get('end_date', None)
        start_date = self.cleaned_data.get('start_date', None)
        if end_date and start_date and self.selected_service.per_night:
            try:
                MinValueValidator(start_date + timezone.timedelta(days=1))(end_date)
            except ValidationError as e:
                self.add_error('end_date', e)

        # Assert people
        adults = self.cleaned_data.get('adults')
        children = self.cleaned_data.get('children')
        seniors = self.cleaned_data.get('seniors')
        people = 0
        if self.selected_service.per_adult and adults:
            people += adults
        if self.selected_service.per_child and children:
            people += children
        if self.selected_service.per_senior and seniors:
            people += seniors
        if self.selected_service.per_adult or self.selected_service.per_child or self.selected_service.per_senior:
            if people <= 0:
                error = gettext_lazy('No people.')
                raise ValidationError(error)

        # Return
        return self.cleaned_data

    def get_field_value(self, name):
        """
        Get a value before validation to set dynamic fields.

        :param name:
        :return:
        """

        field = self.fields[name]
        if field.disabled:
            value = self.get_initial_for_field(field, name)
        else:
            value = field.widget.value_from_datadict(self.data, self.files, self.add_prefix(name))

        try:

            if isinstance(field, FileField):  # pragma: no cover
                initial = self.get_initial_for_field(field, name)

                if value is forms.widgets.FILE_INPUT_CONTRADICTION:
                    value = None
                # False means the field value should be cleared; further validation is
                # not needed.
                if value is False:
                    if not field.required:
                        return False
                    # If the field is required, clearing is not possible (the widget
                    # shouldn't return False data in that case anyway). False is not
                    # in self.empty_value; if a False value makes it this far
                    # it should be validated from here on out as None (so it will be
                    # caught by the required check).
                    value = None
                if not value and initial:
                    value = field.to_python(initial)

            else:
                value = field.to_python(value)

        except ValidationError:
            pass
        ## Clear errors (we only want the value)
        #self._errors = {}

        return value

    @property
    def instance_service(self):
        """
        Returns the show of the provided instance if it exists
        :return: Show
        """
        if self.instance:
            try:
                service = self.instance.service
                return service
            except ObjectDoesNotExist:
                pass
        return None

    def is_valid(self):
        """
        Custom form validation.

        The form should only be considered valid when all fields are ok
        and the final submit button was pressed.
        :return:
        """
        self.is_bound = True
        self._errors = None
        valid = super().is_valid()
        if not self.cleaned_data.get('final_submit', False):
            self._errors = None
            return False
        return valid

    #def remove_input_data(self, field):
    #    """
    #    Removes stored user input from the form submission.

    #    :param field:
    #    :return:
    #    """
    #    data_copy = copy.deepcopy(self.data)
    #    data_copy.pop(field, None)
    #    self.data = data_copy

    def save(self):
        ticketsale = self.instance
        if ticketsale.transaction.closed:
            return ticketsale

        for field in self.fields:
            setattr(ticketsale, field, self.cleaned_data[field])

        ticketsale.per_adult = ticketsale.service.per_adult
        ticketsale.per_child = ticketsale.service.per_child
        ticketsale.per_night = ticketsale.service.per_night
        ticketsale.per_senior = ticketsale.service.per_senior
        ticketsale.per_unit = ticketsale.service.per_unit

        if not ticketsale.per_night:
            ticketsale.end_date = ticketsale.start_date

        ticketsale.save()
        return ticketsale

    def set_choices(self):
        """
        Set dynamic choice fields.

        Selection and choices for fields are set according to post data, and post data is updated to be consistent.
        """
        # Set initial company choices
        self.set_choices_for_type()

        # Set show choices
        self.set_choices_for_service()

    def set_choices_for_type(self):

        # Get available companies
        self.type_choices = apps.get_model('service_sales.ServiceType'). \
            objects.filter(enabled=True, services__enabled=True).distinct().order_by('name')

        # Set field queryset
        self.fields['type'].queryset = self.type_choices

        # Set default selection
        self.selected_type = self.type_choices.first()
        if self.instance_service:
            self.selected_type = self.instance_service.servicetype

        # Update selection according to form input
        servicetype = self.get_field_value('type')
        if servicetype and servicetype in self.type_choices:
            self.selected_type = servicetype

        # Update form input
        self.add_input_data('type', self.selected_type)

    def set_choices_for_service(self):

        # Get available shows
        self.service_choices = apps.get_model('service_sales.Service') \
            .objects.filter(enabled=True, servicetype=self.selected_type).order_by('name')

        # Set field queryset
        self.fields['service'].queryset = self.service_choices

        # Set default selection
        self.selected_service = self.service_choices.first()
        if self.instance_service and self.instance_service in self.service_choices:
            self.selected_service = self.instance_service

        # Update selection according to form input
        service = self.get_field_value('service')
        if service and service in self.service_choices:
            self.selected_service = service

        # Update form input
        self.add_input_data('service', self.selected_service)

    def set_current_values(self):

        # Set values to initial if no input is available
        for key in self.initial:
            if key not in self.data:
                self.add_input_data(key, self.initial[key])

    def set_initial_values(self):

        # Set initial values from instance if the same show is selected
        if self.instance_service == self.selected_service:
            values = {
                'adults': self.instance.adults,
                'children': self.instance.children,
                'type': self.instance_service.servicetype.id,
                'end_date': self.instance.end_date,
                'price_per_adult': self.instance.price_per_adult,
                'price_per_child': self.instance.price_per_child,
                'price_per_senior': self.instance.price_per_senior,
                'price_per_unit': self.instance.price_per_unit,
                'seniors': self.instance.seniors,
                'service': self.instance_service.id,
                'start_date': self.instance.start_date,
                'units': self.instance.units,
            }
        # Set initial values from selected show
        else:
            values = {
                'adults': 2 if self.selected_service.per_adult else 0,
                'children': 0,
                'type': self.selected_service.servicetype,
                'end_date': None,
                'price_per_adult': self.selected_service.price_per_adult,
                'price_per_child': self.selected_service.price_per_child,
                'price_per_senior': self.selected_service.price_per_senior,
                'price_per_unit': self.selected_service.price_per_unit,
                'seniors': 0,
                'service': self.selected_service,
                'start_date': None,
                'units': 1,
            }
        self.initial.update(values)

    def set_layout(self):
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Field('final_submit'),
            Row(
                Column(
                    Field(
                        'type',
                        title=gettext_lazy("Type"),
                        css_class='col-12',
                        onchange='document.getElementById("id_final_submit").value="False";form.submit();',
                    ),
                    css_class='col-6',
                ),
            ),
            Row(
                Column(
                    Field(
                        'service',
                        title=gettext_lazy("Service"),
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
                        css_class='col-12',
                    ),
                    css_class='col-3',
                ),
                Column(
                    Field(
                        'end_date',
                        title=gettext_lazy("End date"),
                        css_class='col-12',
                    ),
                    css_class='col-3',
                ),
            ),
            Row(
                Column(
                    Field(
                        'adults',
                        title=gettext_lazy('Number of adults'),
                        css_class='col-auto',
                    ),
                    AppendedText(
                        'price_per_adult',
                        self.selected_service.currency.symbol,
                        title=gettext_lazy('Price per adult'),
                        css_class='col-auto',
                    ),
                    css_class='col-2',
                ) if self.selected_service.per_adult else None,
                Column(
                    Field(
                        'children',
                        title=gettext_lazy('Number of children'),
                        css_class='col-auto',
                    ),
                    AppendedText(
                        'price_per_child',
                        self.selected_service.currency.symbol,
                        title=gettext_lazy('Price per child'),
                        css_class='col-auto',
                    ),
                    css_class='col-2',
                ) if self.selected_service.per_child else None,
                Column(
                    Field(
                        'seniors',
                        title=gettext_lazy('Number of seniors'),
                        css_class='col-auto',
                    ),
                    AppendedText(
                        'price_per_senior',
                        self.selected_service.currency.symbol,
                        title=gettext_lazy('Price per senior'),
                        css_class='col-auto',
                    ),
                    css_class='col-2',
                ) if self.selected_service.per_senior else None,
                Column(
                    Field(
                        'units',
                        title=gettext_lazy('Number of units'),
                        css_class='col-auto',
                    ),
                    AppendedText(
                        'price_per_unit',
                        self.selected_service.currency.symbol,
                        title=gettext_lazy('Price per unit') if self.selected_service.per_unit else
                        gettext_lazy('Price'),
                        css_class='col-auto',
                    ),
                    css_class='col-2',
                ) if self.selected_service.per_unit or self.selected_service.per_transaction else None,
            ),
        )

    def set_fields(self, *args, **kwargs):
        """
        Sets labels, visibility, requirement, etc...
        """
        # Company
        self.fields['type'].queryset = self.type_choices

        # Show
        self.fields['service'].queryset = self.service_choices

        # Start date
        if not (self.selected_service.date_required or self.selected_service.per_night):
            self.fields['start_date'].widget = forms.HiddenInput()
            self.fields['start_date'].required = False
            self.fields['start_date'].disabled = True

        # End date
        if not self.selected_service.per_night:
            self.fields['end_date'].widget = forms.HiddenInput()
            self.fields['end_date'].required = False
            self.fields['end_date'].disabled = True

        # Adults
        if self.selected_service.per_adult:
            self.fields['price_per_adult'].label = ''
            self.fields['price_per_adult'].disabled = True
            if self.selected_service.variable_price:
                self.fields['price_per_adult'].disabled = False
        else:
            self.fields['adults'].widget = forms.HiddenInput()
            self.fields['adults'].required = False
            self.fields['adults'].disabled = True
            self.fields['price_per_adult'].widget = forms.HiddenInput()
            self.fields['price_per_adult'].required = False
            self.fields['price_per_adult'].disabled = True

        # Children
        if self.selected_service.per_child:
            self.fields['price_per_child'].label = ''
            self.fields['price_per_child'].disabled = True
            if self.selected_service.variable_price:
                self.fields['price_per_child'].disabled = False
        else:
            self.fields['children'].widget = forms.HiddenInput()
            self.fields['children'].required = False
            self.fields['children'].disabled = True
            self.fields['price_per_child'].widget = forms.HiddenInput()
            self.fields['price_per_child'].required = False
            self.fields['price_per_child'].disabled = True

        # Seniors
        if self.selected_service.per_senior:
            self.fields['price_per_senior'].label = ''
            self.fields['price_per_senior'].disabled = True
            if self.selected_service.variable_price:
                self.fields['price_per_senior'].disabled = False
        else:
            self.fields['seniors'].widget = forms.HiddenInput()
            self.fields['seniors'].required = False
            self.fields['seniors'].disabled = True
            self.fields['price_per_senior'].widget = forms.HiddenInput()
            self.fields['price_per_senior'].required = False
            self.fields['price_per_senior'].disabled = True

        # Units
        self.fields['price_per_unit'].disabled = not self.selected_service.variable_price
        if self.selected_service.per_unit:
            self.fields['price_per_unit'].label = ''
        else:
            self.fields['units'].widget = forms.HiddenInput()
            self.fields['units'].required = False
            self.fields['units'].disabled = True
            self.fields['price_per_unit'].label = gettext_lazy('Price')
            if not self.selected_service.per_transaction:
                self.fields['price_per_unit'].widget = forms.HiddenInput()
                self.fields['price_per_unit'].required = False
                self.fields['price_per_unit'].disabled = True

        # Disable all if transaction is closed
        if self.instance and self.instance.transaction.closed:
            for field in self.fields:
                self.fields[field].disabled = True

