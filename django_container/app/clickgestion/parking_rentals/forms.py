from django.apps import apps
from clickgestion.parking_rentals.models import ParkingRental
from clickgestion.apt_rentals.forms import AptRentalForm


class ParkingRentalForm(AptRentalForm):

    class Meta:
        model = ParkingRental
        fields = ('end_date', 'start_date')

    def save(self, commit=True):
        parkingrental = super().save(commit=False)
        if commit:
            parkingrental.save()
            if self.cleaned_data['add_deposit']:
                deposit = apps.get_model('deposits.parkingrentaldeposit')(parkingrental=parkingrental)
                deposit.save()
        return parkingrental
