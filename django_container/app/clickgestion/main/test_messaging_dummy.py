from littleserverdjango.littleserver_core.test import LittleServerTestCase
from littleserverdjango.littleserver_core import messaging_dummy


class TestMessagingDummy(LittleServerTestCase):

    def test_get_commlink_display_address(self):
        assert messaging_dummy.get_commlink_display_address(self.local_commlink)

    def test_process_message(self):
        assert not messaging_dummy.process_message({'type': 'connection_message'})

    def test_stop_commlink(self):
        assert messaging_dummy.stop_commlink(self.local_commlink)

