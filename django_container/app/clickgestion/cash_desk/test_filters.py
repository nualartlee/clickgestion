from clickgestion.core.test import CustomTestCase
from clickgestion.cash_desk.filters import CashCloseFilter


class CashCloseFilterTest(CustomTestCase):

    def test_filter_ok(self):
        filter_data = {}
        filter = CashCloseFilter(data=filter_data)
        self.assertTrue(filter.is_valid())

    def test_filter_code(self):

        # Initial returned
        filter_data = {
            'notes': 'ma',
        }
        filter = CashCloseFilter(data=filter_data)
        self.assertTrue(filter.is_valid())
