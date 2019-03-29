from clickgestion.core.test import CustomTestCase
from clickgestion.concepts import totalizers
from clickgestion.concepts.models import BaseConcept
from clickgestion.core.model_creation import create_test_models


class TestTotalizers(CustomTestCase):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        print('creating test models')
        create_test_models(days=7)

    def test_get_breakdown_by_accounting_group(self):
        assert totalizers.get_breakdown_by_accounting_group()
        assert totalizers.get_breakdown_by_accounting_group(BaseConcept.objects.all())

    def test_get_breakdown_by_concept_type(self):
        assert totalizers.get_breakdown_by_concept_type()
        assert totalizers.get_breakdown_by_concept_type(BaseConcept.objects.all())

    def test_get_breakdowns_by_accounting_group_by_employee(self):
        assert totalizers.get_breakdowns_by_accounting_group_by_employee()
        assert totalizers.get_breakdowns_by_accounting_group_by_employee(BaseConcept.objects.all())

    def test_get_breakdowns_by_concept_type_by_employee(self):
        assert totalizers.get_breakdowns_by_concept_type_by_employee()
        assert totalizers.get_breakdowns_by_concept_type_by_employee(BaseConcept.objects.all())

    def test_get_deposits_in_holding_breakdown(self):
        assert totalizers.get_deposits_in_holding_breakdown()

    def test_get_deposits_in_holding_concepts(self):
        assert totalizers.get_deposits_in_holding_concepts()

    def test_get_deposits_in_holding_totals(self):
        assert totalizers.get_deposits_in_holding_totals()

