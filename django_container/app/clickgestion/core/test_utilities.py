from django.apps import apps
from clickgestion.core import model_creation
from clickgestion.core.utilities import custom_permission_required
from clickgestion.core.test import CustomTestCase
from unittest.mock import Mock


class UtilitiesTest(CustomTestCase):

    def test_custom_permission_redirect(self):
        testuser = model_creation.create_user('testuser', 'testuser', 'testuser', 't@t.com', [])
        required_permission = 'apt_rentals.add_aptrental'
        codename = required_permission.split('.')[1]
        permission = apps.get_model('auth.Permission').objects.get(codename=codename)
        # No permission
        testuser.user_permissions.remove(permission)
        testuser.save()
        self.client.force_login(testuser)
        request = Mock()
        request.user = Mock(return_value=testuser)
        view = Mock()
        response = custom_permission_required(permission)(view)(request)
        self.assertEqual(type(response), Mock)
        import pdb; pdb.set_trace()



