from unittest import mock
from littleserverdjango.littleserver_core.test import LittleServerTestCase
from littleserverdjango.littleserver_core import encryption, messaging, messages


class TestMessaging(LittleServerTestCase):

    def test_compress(self):
        assert messaging._compress("message")

    def test_decompress(self):
        assert messaging._decompress("compressed_message")

    def test_deserialize(self):
        message = {"message": "this message"}
        serialized = messaging._serialize(message)
        deserialized = messaging._deserialize(serialized)
        assert message == deserialized

    @mock.patch('littleserverdjango.littleserver_core.messaging.process_message')
    def test_dispatch_message(self, mock_process_message):
        keepalive_message = {
            'type': 'keepalive',
            'app': 'littleserver',
            'content': 'Are you alive?',
            'valid': True,
            'uuid': "11111AAAAA",
            'sender': self.local_server,
            'module': 'littleserver_core.messaging_dummy'
        }
        result = messaging.dispatch_message(keepalive_message)
        mock_process_message.assertCalled()

    def test_process_invalid_message(self):
        assert not messaging._process_invalid_message("message")

    @mock.patch('littleserverdjango.littleserver_core.messaging.send_message')
    def test_process_keepalive_message(self, mock_send_message):
        message = {
            'uuid': 'aaa',
            'sender': 'me',
            'cryptotool': mock.Mock(commlink=self.remote_commlink),
            'received_timestamp': 'now',
        }
        messaging._process_keepalive_message(message)
        assert mock_send_message.call_count == 1

    def test_process_keepalive_response_message(self):
        assert not messaging._process_keepalive_response_message("message")

    @mock.patch('littleserverdjango.littleserver_core.messaging.dispatch_message')
    @mock.patch('littleserverdjango.littleserver_core.messaging._process_keepalive_response_message')
    @mock.patch('littleserverdjango.littleserver_core.messaging._process_keepalive_message')
    @mock.patch('littleserverdjango.littleserver_core.messaging._process_unknown_message')
    @mock.patch('littleserverdjango.littleserver_core.messaging._process_invalid_message')
    def test_process_message(self, mock_invalid, mock_unknown, mock_keepalive, mock_keepalive_response, mock_dispatch):
        # Invalid
        message = {
            'type': 'keepalive',
            'module': 'littleserverdjango.littleserver_core.messaging',
        }
        messaging.process_message(message)
        assert mock_invalid.call_count == 1
        assert mock_keepalive.call_count == 0
        assert mock_keepalive_response.call_count == 0
        assert mock_unknown.call_count == 0
        assert mock_dispatch.call_count == 0

        # Keepalive
        mock_commlink = mock.Mock(name='mock_commlink')
        mock_cryptotool = mock.Mock(commlink=mock_commlink)
        message = {
            'type': 'keepalive',
            'valid': True,
            'module': 'littleserverdjango.littleserver_core.messaging',
            'cryptotool': mock_cryptotool,
        }
        messaging.process_message(message)
        assert mock_invalid.call_count == 1
        assert mock_keepalive_response.call_count == 0
        assert mock_keepalive.call_count == 1
        assert mock_unknown.call_count == 0
        assert mock_dispatch.call_count == 0

        # Keepalive response
        mock_commlink = mock.Mock(name='mock_commlink')
        mock_cryptotool = mock.Mock(commlink=mock_commlink)
        message = {
            'type': 'keepalive_response',
            'valid': True,
            'module': 'littleserverdjango.littleserver_core.messaging',
            'cryptotool': mock_cryptotool,
        }
        messaging.process_message(message)
        assert mock_invalid.call_count == 1
        assert mock_keepalive_response.call_count == 1
        assert mock_keepalive.call_count == 1
        assert mock_unknown.call_count == 0
        assert mock_dispatch.call_count == 0

        # Unknown
        message = {
            'type': 'unknown',
            'valid': True,
            'module': 'littleserverdjango.littleserver_core.messaging',
        }
        messaging.process_message(message)
        assert mock_invalid.call_count == 1
        assert mock_keepalive.call_count == 1
        assert mock_keepalive_response.call_count == 1
        assert mock_unknown.call_count == 1
        assert mock_dispatch.call_count == 0

        # Other
        message = {
            'type': 'unknown',
            'valid': True,
            'module': 'littleserverdjango.littleserver_core.other',
        }
        messaging.process_message(message)
        assert mock_invalid.call_count == 1
        assert mock_keepalive.call_count == 1
        assert mock_keepalive_response.call_count == 1
        assert mock_unknown.call_count == 1
        assert mock_dispatch.call_count == 1

    def test_process_unknown_message(self):
        assert messaging._process_unknown_message('none')

    @mock.patch('littleserverdjango.littleserver_core.messaging._process_raw_message_inner')
    def test_process_raw_message(self, mock_inner):
        messaging.process_raw_message('message')
        assert mock_inner.delay.call_count == 1

    @mock.patch('littleserverdjango.littleserver_core.messaging.process_message')
    @mock.patch('littleserverdjango.littleserver_core.encryption.decrypt_message')
    def test_process_raw_message_inner(self, mock_decrypt, mock_process_message):
        mock_decrypt.return_value = False, False
        # bad
        messaging._process_raw_message_inner("bad")
        assert mock_process_message.call_count == 0
        # plaintext
        message = {
            'type': 'connection',
            'plaintext': True,
        }
        serialized = messaging._serialize(message)
        messaging._process_raw_message_inner(serialized)
        assert mock_process_message.call_count == 1
        # encrypted
        message = messaging._serialize(messages.keepalive_message())
        mock_decrypt.return_value = self.local_commlink.cryptotool, message
        messaging._process_raw_message_inner("encrypted")
        assert mock_process_message.call_count == 2
        # encrypted no cryptotool
        message = messaging._serialize(messages.keepalive_message())
        mock_decrypt.return_value = None, message
        messaging._process_raw_message_inner("encrypted")
        assert mock_process_message.call_count == 3

    def test_retrieve_plaintext_message(self):
        # good message
        message = {
            'type': 'connection',
        }
        serialized_message = messaging._serialize(message)
        assert messaging._retrieve_plaintext_message(serialized_message)
        # bad message
        message = 'bad'
        serialized_message = messaging._serialize(message)
        assert not messaging._retrieve_plaintext_message(serialized_message)
        # unknown message
        message = {
            'type': 'strange',
        }
        serialized_message = messaging._serialize(message)
        assert not messaging._retrieve_plaintext_message(serialized_message)

    def test_send_encrypted_message(self):
        message = {
            'type': 'test',
        }
        assert messaging._send_encrypted_message(self.remote_commlink, message)

    @mock.patch('littleserverdjango.littleserver_core.messaging._send_message_inner')
    def test_send_message_async(self, mock_inner):
        # no result actions
        messaging._send_message_async('recipient', 'message')
        assert mock_inner.call_count == 1
        # success result actions
        mock_inner.return_value = True
        result_actions = {
            'success_action': print,
            'success_action_args': ('success result actions executed',),
        }
        messaging._send_message_async('recipient', 'message', result_actions=result_actions)
        assert mock_inner.call_count == 2
        # failure result actions
        mock_inner.return_value = False
        result_actions = {
            'failure_action': print,
            'failure_action_args': ('failure result actions executed',),
        }
        messaging._send_message_async('recipient', 'message', result_actions=result_actions)
        assert mock_inner.call_count == 3
        # empty result actions
        mock_inner.return_value = False
        result_actions = {
            'success_action_args': ('success result actions executed',),
            'failure_action_args': ('failure result actions executed',),
        }
        messaging._send_message_async('recipient', 'message', result_actions=result_actions)
        assert mock_inner.call_count == 4

    @mock.patch('littleserverdjango.littleserver_core.messaging._send_message_inner')
    @mock.patch('littleserverdjango.littleserver_core.messaging._send_message_async')
    def test_send_message(self, mock_async, mock_inner):
        messaging.send_message('recipient', 'message')
        assert mock_async.delay.call_count == 1
        messaging.send_message('recipient', 'message', async=False)
        assert mock_inner.call_count == 1

    @mock.patch('littleserverdjango.littleserver_core.messaging._send_encrypted_message')
    @mock.patch('littleserverdjango.littleserver_core.messaging._send_plaintext_message')
    def test_send_message_inner(self, mock_send_plaintext, mock_send_encrypted):
        # to a cryptotool, in plaintext
        message = {
            'plaintext': True,
            'type': 'Test Message',
            'module': 'littleserverdjango.littleserver_core.messaging',
        }
        messaging._send_message_inner(self.remote_commlink, message)
        mock_send_plaintext.assertCalledWith(self.remote_commlink, message)
        # to a server, encrypted
        message = {
            'type': 'test',
            'module': 'littleserverdjango.littleserver_core.messaging',
        }
        messaging._send_message_inner(self.local_server, message)
        mock_send_plaintext.assertCalledWith(self.remote_commlink, message)

    def test_send_plaintext_message(self):
        message = {
            'plaintext': True
        }
        assert messaging._send_plaintext_message(self.remote_commlink, message)

    def test_serialize(self):
        # bad
        message = {
            'serve': self.local_server,
        }
        self.assertRaises(TypeError, messaging._serialize, message)
        # good
        message = {
            'type': 'test',
        }
        assert messaging._serialize(message)

    def test_set_message_metadata(self):
        message = {
            'type': 'test',
        }
        message = messaging._set_message_metadata(self.remote_commlink, message)
        assert message['uuid']
        assert message['sent_timestamp']

    def test_set_response_metadata(self):
        message = {
            'type': 'test',
            'received_timestamp': 'none',
        }
        message = messaging._set_message_metadata(self.remote_commlink, message)
        message = messaging._set_response_metadata(message)
        assert message['response_to'] == message['uuid']
        assert not message.get('received_timestamp', False)

    @mock.patch('littleserverdjango.littleserver_core.messaging._setup_communication_modules')
    def test_setup_communications(self, mock_setup_comm_mods):
        messaging.setup_communications()
        mock_setup_comm_mods.assertCalled()

    def test_setup_communication_modules(self):
        messaging._setup_communication_modules()

    @mock.patch('littleserverdjango.littleserver_core.messaging._start_communication_modules')
    def test_start_communications(self, mock_start_comm_mods):
        messaging.start_communications()
        mock_start_comm_mods.assertCalled()

    def test_start_communication_modules(self):
        messaging._start_communication_modules()






