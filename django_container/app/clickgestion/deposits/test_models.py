from clickgestion.core.test import CustomTestCase
from clickgestion.deposits.models import DepositReturn


class TestDepositReturn(CustomTestCase):

    def test_model(self):
        depositreturn = DepositReturn(transaction=self.transaction, returned_deposit=self.apartment_rental_deposit)
        depositreturn.save()
        assert depositreturn

