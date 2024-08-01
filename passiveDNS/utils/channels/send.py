from multiprocessing import Process

import logging

from passiveDNS.utils import timezone, config
from passiveDNS.utils.channels.redis import send_redis
from passiveDNS.utils.channels.templates_list import ALERT_DN_TEMPLATE, TEST_TEMPLATE
from passiveDNS.models.channel import Channel
from passiveDNS.models.channel_meta import (
    ChannelRedis,
)

send_channels = {
    ChannelRedis.TYPE: send_redis,
}


def send(channel: Channel, template):
    """
    Send a template to a user through a particular channel
    :param to: the user contact
    :param channel: the channel to use
    :param template: the message to send
    :return:
    """
    if channel.type not in send_channels:
        raise ValueError("Channel type not supported")

    send_channels[channel.type](channel, template)


def test_send(channel: Channel):
    template = TEST_TEMPLATE
    template.set_format(date=timezone.get_current_datetime(config.g.TIMEZONE))
    logging.debug(f"sending test message to {channel.name}")
    send(channel, template)


def alert_all_process(domain_name):
    """
    Sent the DN list to all registered Users
    :param domain_name: the domain name to send
    :return:
    """

    data = {
        "domain name": domain_name["domain_name"],
        "last ip": domain_name["last_ip_address"],
        "current ip": domain_name["current_ip_address"],
    }
    logging.debug(f"Data: {data}")

    template = ALERT_DN_TEMPLATE
    template.set_format(
        date=timezone.get_current_datetime(config.g.TIMEZONE), data=data
    )

    channels = Channel.list()
    for c in channels:
        logging.debug(f"alerting about {domain_name["domain_name"]} with {c.name}")
        send(c, template)


def alert_all_dn(domain_name):
    """
    Start a new process to alert all users asynchronously
    :param domain_name: the domain name to send
    :return:
    """
    p = Process(target=alert_all_process, args=(domain_name,))
    p.start()
