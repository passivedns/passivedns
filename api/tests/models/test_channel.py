from unittest import TestCase
from unittest.mock import MagicMock

from models.channel import Channel, ChannelTypeError

channel_email = {
    "_key": "email_chan",
    "type": "email",
    "infos": {
        "smtp_host": "host",
        "smtp_port": "port",
        "sender_email": "email",
        "sender_password": "password",
    }
}

channel_telegram = {
    "_key": "tel_chan",
    "type": "telegram",
    "infos": {
        "bot_token": "token"
    }
}

CHANNEL_NAME = "new_chan"


class TestChannel(TestCase):
    def test_init_email(self):
        ch = Channel.new(
            CHANNEL_NAME, channel_email['type'], channel_email['infos']
        )
        self.assertEqual(ch.name, CHANNEL_NAME)
        self.assertEqual(ch.infos.smtp_host, channel_email['infos']['smtp_host'])
        self.assertEqual(ch.infos.smtp_port, channel_email['infos']['smtp_port'])
        self.assertEqual(ch.infos.sender_email, channel_email['infos']['sender_email'])
        self.assertEqual(ch.infos.sender_password, channel_email['infos']['sender_password'])

    def test_init_telegram(self):
        ch = Channel.new(
            CHANNEL_NAME, channel_telegram['type'], channel_telegram['infos']
        )
        self.assertEqual(ch.name, CHANNEL_NAME)
        self.assertEqual(ch.infos.bot_token, channel_telegram['infos']['bot_token'])

    def test_init_error(self):
        with self.assertRaises(ChannelTypeError):
            Channel.new(
                CHANNEL_NAME, "stuff", {}
            )

    def test_get_email(self):
        name = channel_email['_key']
        Channel._get = MagicMock(return_value=channel_email)
        ch = Channel.get(name)
        self.assertEqual(ch.name, name)
        self.assertEqual(ch.infos.smtp_host, channel_email['infos']['smtp_host'])
        self.assertEqual(ch.infos.smtp_port, channel_email['infos']['smtp_port'])
        self.assertEqual(ch.infos.sender_email, channel_email['infos']['sender_email'])
        self.assertEqual(ch.infos.sender_password, channel_email['infos']['sender_password'])

    def test_get_telegram(self):
        name = channel_telegram['_key']
        Channel._get = MagicMock(return_value=channel_telegram)
        ch = Channel.get(name)
        self.assertEqual(ch.name, name)
        self.assertEqual(ch.infos.bot_token, channel_telegram['infos']['bot_token'])

    def test_list(self):
        Channel._list = MagicMock(return_value=[
            channel_email,
            channel_telegram
        ])
        ch_list = Channel.list()
        self.assertEqual(len(ch_list), 2)
        self.assertEqual(ch_list[0].type, channel_email['type'])
        self.assertEqual(ch_list[1].type, channel_telegram['type'])


