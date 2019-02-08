from clickgestion.main.test import CustomTestCase
from clickgestion.main import forms
from unittest import skip


@skip
class TestDefaultDeleteForm(CustomTestCase):

    def test_form_ok(self):
        form_data = {}
        form = forms.DefaultDeleteForm(referer='/')
        self.assertFalse(form.is_valid())


