from clickgestion.concepts.test_models import BaseConceptModelTest


class TestSafeRental(BaseConceptModelTest):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_object = cls.saferental
