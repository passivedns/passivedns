import os
from unittest import TestCase
from datetime import datetime

from channels.telegram import send_telegram
from channels.templates_list import TEST_TEMPLATE
from models.channel import Channel
from models.channel_meta import ChannelTelegram

channel_telegram = Channel.new(
    "test", ChannelTelegram.TYPE, {"bot_token": os.environ["TELEGRAM_BOT_TOKEN"]}
)

chat_id = os.environ["CHAT_ID"]


class TestTelegram(TestCase):
    def test_send(self):
        template = TEST_TEMPLATE
        template.set_format(date=str(datetime.now().date()))
        send_telegram(chat_id, channel_telegram.infos, template)
