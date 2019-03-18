from clickgestion.core.test import CustomTestCase
from clickgestion.cash_desk.filters import CashCloseFilter
from django.utils import timezone


class CashCloseFilterTest(CustomTestCase):

    def test_filter_ok(self):
        filter_data = {
            'adults': 2,
            'children': 0,
            'start_date': timezone.now(),
            'end_date': timezone.now() + timezone.timedelta(days=7),
        }
        filter = CashCloseFilter(data=filter_data)
        self.assertTrue(filter.is_valid())
