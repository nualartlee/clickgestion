from clickgestion.core.test import CustomTestCase
from clickgestion.cash_desk.models import CashClose
from clickgestion.cash_desk.models import get_breakdown_by_concept_type, get_new_cashclose_code, get_value_totals
from unittest import skip


class TestGetNewCashCloseCode(CustomTestCase):

    def test_get_new_cashclose_code(self):
        code = get_new_cashclose_code()
        assert code


@skip
class TestCashClose(CustomTestCase):

    def test_str(self):
        assert self.cashclose.__str__()


