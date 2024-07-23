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
    r = redis.Redis(host=channel.infos.host, port=channel.infos.port, db=channel.infos.db)
    r.publish(channel.infos.queue_name, template.get_redis_msg())
