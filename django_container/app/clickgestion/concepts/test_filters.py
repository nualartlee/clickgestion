from clickgestion.core.test import CustomTestCase
from clickgestion.concepts.filters import ConceptFilter
from clickgestion.core import model_creation
from django.utils import timezone


class TestConceptFilter(CustomTestCase):

    def test_filter_ok(self):

        # Initial returned
        filter_data = {
        }
        filter = ConceptFilter(data=filter_data)
        #import pdb;pdb.set_trace()
