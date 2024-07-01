import requests

from passiveDNS.utils.channels.templates import ChannelTemplate
from passiveDNS.models.channel_meta import ChannelTelegram


class TelegramSendingError(Exception):
    pass


def send_telegram(chat_id: str, channel: ChannelTelegram, template: ChannelTemplate):
    """
    Send a message through the Telegram channel
    :param chat_id: where to send the message
    :param channel: the bot token
    :param template: the message to send
    :return:
    :raise: TelegramSendingError if message not sent
    """
    url = "https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id}&text={msg}&parse_mode={parse_mode}".format(
        bot_id=channel.bot_token,
        chat_id=chat_id,
        msg=template.get_telegram_msg(),
        parse_mode=template.telegram.parse_mode,
    )

    r = requests.get(url)
    if r.status_code != 200:
        raise TelegramSendingError
