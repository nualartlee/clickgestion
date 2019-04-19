from django.apps import apps
from clickgestion.safe_rentals.models import SafeRental
from clickgestion.apt_rentals.forms import AptRentalForm


class SafeRentalForm(AptRentalForm):

    class Meta:
        model = SafeRental
        fields = ('end_date', 'start_date')

    def save(self, commit=True):
        saferental = super().save(commit=False)
        if commit:
            saferental.save()
            if self.cleaned_data['add_deposit']:
                deposit = apps.get_model('deposits.saferentaldeposit')(saferental=saferental)
                deposit.save()
        return saferental
