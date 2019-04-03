from clickgestion.concepts.test_models import BaseConceptModelTest


class TestParkingRental(BaseConceptModelTest):

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.model_object = cls.parkingrental
