from clickgestion.core.test import CustomTestCase
from clickgestion.deposit_returns.models import DepositReturn
from clickgestion.apt_rentals.models import AptRentalDeposit


class TestDepositReturn(CustomTestCase):

    def test_model(self):
        deposit_return = DepositReturn(transaction=self.transaction, returned_deposit=self.apartment_rental_deposit)
        deposit_return.save()
        assert deposit_return

