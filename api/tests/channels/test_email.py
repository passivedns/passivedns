import os
from unittest import TestCase
from datetime import datetime

from channels.email import send_email
from channels.templates_list import TEST_TEMPLATE
from models.channel import Channel
from models.channel_meta import ChannelEmail

channel_email = Channel.new("test", ChannelEmail.TYPE, {
    "smtp_host": "mail.gmx.com",
    "smtp_port": "587",
    "sender_email": "dadard.website@gmx.com",
    "sender_password": os.environ['SMTP_PASSWORD']
})

user_mail = "florian.charpentier67@gmail.com"


class TestEmail(TestCase):
    def test_send(self):
        template = TEST_TEMPLATE
        template.set_format(date=str(datetime.now().date()))
        send_email(user_mail, channel_email.infos, template)
