from multiprocessing import Process

import pandas
import logging

from passiveDNS.utils.channels.email import send_email
from passiveDNS.utils.channels.redis import send_redis
from passiveDNS.utils.channels.templates_list import ALERT_LIST_TEMPLATE
from passiveDNS.models.channel import Channel
from passiveDNS.models.user_channel import UserChannel
from passiveDNS.models.user import User, UserRole
from passiveDNS.models.channel_meta import (
    ChannelEmail,
    ChannelRedis,
)

send_channels = {
    ChannelEmail.TYPE: send_email,
    ChannelRedis.TYPE: send_redis,
}


def send(to: str, channel: Channel, template):
    """
    Send a template to a user through a particular channel
    :param to: the user contact
    :param channel: the channel to use
    :param template: the message to send
    :return:
    """
    if channel.type not in send_channels:
        raise ValueError("Channel type not supported")

    send_channels[channel.type](to, channel, template)


def alert_all_process(dn_list):
    """
    Sent the DN list to all registered Users
    :param dn_list: the DN list to send
    :return:
    """

    data = []
    for dn in dn_list:
        data.append(
            [
                dn["domain_name"],
                dn["last_ip_address"],
                dn["current_ip_address"],
            ]
        )
    logging.debug(f"Data: {data}")
    columns = ["Domain name", "Last IP address", "Current IP address"]
    df = pandas.DataFrame(data=data, columns=columns)

    # fixme
    template = ALERT_LIST_TEMPLATE
    template.set_format(
        url_alerts="/alerts",
        url_channels="/channels",
        table=df.to_markdown(index=False),
    )

    # fixme
    # users = User.list()
    users = [User.get("user")]
    for u in users:
        if u.role != UserRole.USER.value and u.role != UserRole.ADMIN.value:
            continue

        user_channels = UserChannel.list_from_username(u.username)
        logging.debug(f"User Channel: {user_channels}")
        for u_ch in user_channels:
            channel = Channel.get(u_ch.channel_name)
            logging.debug(f"alerting {u_ch.contact} with {channel.type}")
            send(u_ch.contact, channel, template)


def alert_all(dn_list):
    """
    Start a new process to alert all users asynchronously
    :param dn_list: the DN list to send
    :return:
    """
    p = Process(target=alert_all_process, args=(dn_list,))
    p.start()
