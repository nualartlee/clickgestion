from unittest import mock
from littleserverdjango.littleserver_core.test import LittleServerTestCase
from littleserverdjango.littleserver_core import messaging, messages


class TestMessages(LittleServerTestCase):

    def test_connection_message(self):
        assert messages.connection_message()

    def test_keepalive_message(self):
        assert messages.keepalive_message()

    def test_keepalive_response_message(self):
        assert messages.keepalive_response_message()

    def test_notification_message(self):
        assert messages.notification_message()

    def test_set_message_kwargs(self):
        message = messages.notification_message(
            title='1',
            header='2',
            body='3',
        )
        assert message['title'] == '1'
        assert message['header'] == '2'
        assert message['body'] == '3'
