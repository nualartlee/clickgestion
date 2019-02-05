from littleserverdjango.littleserver_core.test import LittleServerTestCase
from littleserverdjango.littleserver_core import forms


class TestDefaultDeleteForm(LittleServerTestCase):

    def test_form_ok(self):
        form_data = {}
        form = forms.DefaultDeleteForm(referer='/home')
        self.assertFalse(form.is_valid())


