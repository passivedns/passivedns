import redis
from passiveDNS.utils.channels.templates import ChannelTemplate
from passiveDNS.models.channel_meta import ChannelRedis


def send_redis(channel: ChannelRedis, template: ChannelTemplate):
    """
    Send a message to a user through Redis
    :param channel: Redis Configuration
    :param template: the message to send
    :return:
    """
    r = redis.Redis(host=channel.host, port=channel.port, db=channel.db)
    r.lpush(channel.queue, template.get_redis_msg())
