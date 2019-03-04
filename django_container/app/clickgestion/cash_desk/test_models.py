from clickgestion.core.test import CustomTestCase
from clickgestion.cash_desk.models import get_new_cashclose_code
from unittest import skip


class TestGetNewCashCloseCode(CustomTestCase):

    def test_get_new_cashclose_code(self):
        code = get_new_cashclose_code()
        assert code


@skip
class TestCashClose(CustomTestCase):

    def test_str(self):
        assert self.cashclose.__str__()


