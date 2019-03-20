from django.apps import apps
from clickgestion.core import model_creation
from clickgestion.core.utilities import custom_permission_required
from clickgestion.core.test import CustomTestCase
from unittest.mock import Mock
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404


class UtilitiesTest(CustomTestCase):

    def test_custom_permission_redirect(self):
        testuser = model_creation.create_user('testuser', 'testuser', 'testuser', 't@t.com', [])
        required_permission = 'apt_rentals.add_aptrental'
        codename = required_permission.split('.')[1]
        permission = apps.get_model('auth.Permission').objects.get(codename=codename)

        # Not logged in
        request = Mock()
        request.configure_mock(user=AnonymousUser())
        return_view = 'mockview'
        view = Mock(return_value=return_view)
        view.request = Mock(return_value=request)
        response = custom_permission_required(required_permission)(view)(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/')

        # No permission
        request = Mock()
        request.configure_mock(user=testuser)
        return_view = 'mockview'
        view = Mock(return_value=return_view)
        self.assertRaises(PermissionDenied, custom_permission_required(required_permission)(view), request)

        # Has permission
        print('has permission')
        testuser.user_permissions.add(permission)
        testuser.save()
        testuser = get_object_or_404(get_user_model(), id=testuser.id)
        request = Mock()
        request.configure_mock(user=testuser)
        return_view = 'mockview'
        view = Mock(return_value=return_view)
        response = custom_permission_required(required_permission)(view)(request)
        self.assertEqual(response, return_view)



