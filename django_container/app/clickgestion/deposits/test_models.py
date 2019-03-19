from clickgestion.core.test import CustomTestCase
from clickgestion.deposits.models import DepositReturn


class TestDepositReturn(CustomTestCase):

    def test_model(self):
        depositreturn = DepositReturn(transaction=self.transaction, returned_deposit=self.aptrentaldeposit)
        depositreturn.save()
        assert depositreturn

