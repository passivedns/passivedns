import os
from unittest import TestCase
from datetime import datetime

from channels.discord_chan import send_discord
from models.channel import Channel
from models.channel_meta import ChannelDiscord
from channels.templates_list import TEST_TEMPLATE

channel_discord = Channel.new(
    "discord", ChannelDiscord.TYPE, {"bot_token": os.environ["DISCORD_BOT_TOKEN"]}
)

user_id = os.environ["DISCORD_USER_ID"]


class TestDiscord(TestCase):
    def test_send(self):
        template = TEST_TEMPLATE
        template.set_format(date=str(datetime.now().date()))
        send_discord(user_id, channel_discord.infos, template)
