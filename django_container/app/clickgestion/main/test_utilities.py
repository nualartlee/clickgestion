from littleserverdjango.littleserver_core.test import LittleServerTestCase
from django.utils import timezone
from littleserverdjango.littleserver_core import utilities
from unittest import mock
from django.core.exceptions import PermissionDenied
from django.shortcuts import reverse


class TestUtilitites(LittleServerTestCase):

    def test_invalid_permission_redirect(self):
        mock_user = mock.Mock(is_authenticated=True)
        mock_request = mock.Mock(user=mock_user, path='path')
        self.assertRaises(PermissionDenied, utilities.invalid_permission_redirect, mock_request)
        mock_user = mock.Mock(is_authenticated=False)
        mock_request = mock.Mock(user=mock_user)
        response = utilities.invalid_permission_redirect(mock_request)
        self.assertEqual(response.url, reverse('login'))
        self.assertEqual(response.status_code, 302)

    def test_time_delta_to_text(self):
        # nothing
        result = utilities.timedelta_to_text(None)
        assert '(not known)' in result
        # a few seconds ago
        timestamp = timezone.now()
        result = utilities.timedelta_to_text(timestamp)
        assert 'a few seconds ago' in result
        # a minute ago
        timestamp = timezone.now() - timezone.timedelta(minutes=1.5)
        result = utilities.timedelta_to_text(timestamp)
        assert 'a minute ago' in result
        # minutes ago
        timestamp = timezone.now() - timezone.timedelta(minutes=3)
        result = utilities.timedelta_to_text(timestamp)
        assert 'minutes ago' in result
        # an hour ago
        timestamp = timezone.now() - timezone.timedelta(hours=1.5)
        result = utilities.timedelta_to_text(timestamp)
        assert 'an hour ago' in result
        # hours ago
        timestamp = timezone.now() - timezone.timedelta(hours=2)
        result = utilities.timedelta_to_text(timestamp)
        assert 'hours ago' in result
        # yesterday
        timestamp = timezone.now() - timezone.timedelta(days=1.5)
        result = utilities.timedelta_to_text(timestamp)
        assert 'yesterday' in result
        # days ago
        timestamp = timezone.now() - timezone.timedelta(days=3)
        result = utilities.timedelta_to_text(timestamp)
        assert 'days ago' in result
        # in a few seconds
        timestamp = timezone.now() + timezone.timedelta(seconds=30)
        result = utilities.timedelta_to_text(timestamp)
        assert 'in a few seconds' in result
        # in a minute
        timestamp = timezone.now() + timezone.timedelta(minutes=1.5)
        result = utilities.timedelta_to_text(timestamp)
        assert 'in a minute' in result
        # in 3 minutes
        timestamp = timezone.now() + timezone.timedelta(minutes=3.5)
        result = utilities.timedelta_to_text(timestamp)
        assert 'in 3 minutes' in result
        # in an hour
        timestamp = timezone.now() + timezone.timedelta(hours=1.5)
        result = utilities.timedelta_to_text(timestamp)
        assert 'in an hour' in result
        # in 2 hours
        timestamp = timezone.now() + timezone.timedelta(hours=2.5)
        result = utilities.timedelta_to_text(timestamp)
        assert 'in 2 hours' in result
        # tomorrow
        timestamp = timezone.now() + timezone.timedelta(days=1.5)
        result = utilities.timedelta_to_text(timestamp)
        assert 'tomorrow' in result
        # in days
        timestamp = timezone.now() + timezone.timedelta(days=3.5)
        result = utilities.timedelta_to_text(timestamp)
        assert 'in 3 days' in result


