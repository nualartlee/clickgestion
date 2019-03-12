from clickgestion.core.test import CustomTestCase
from clickgestion.concepts.totalizers import get_breakdown_by_accounting_group, get_deposits_in_holding
from clickgestion.concepts.models import BaseConcept
from clickgestion.core.model_creation import create_test_models


class TestTotalizers(CustomTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        print('creating test models')
        create_test_models(days=7)

    def test_get_breakdown_by_accounting_group(self):
        assert get_breakdown_by_accounting_group(BaseConcept.objects.all())

    def test_get_deposits_in_holding(self):
        assert get_deposits_in_holding()

