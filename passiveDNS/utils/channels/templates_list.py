from passiveDNS.utils.channels.templates import (
    ChannelTemplate,
    RedisTemplate,
)

TEST_TEMPLATE = ChannelTemplate(
    RedisTemplate(
        """{date}: **Testing** channel redis"""
    ),
)

INVITE_TEMPLATE = ChannelTemplate(
    RedisTemplate(
        """
        You have been invited by the admin of Passive DNS to join in, as a user.
        Cheers,
        """
    ),
)

CHANNEL_VERIFY_TEMPLATE = ChannelTemplate(
    RedisTemplate(
        """
        **Passive DNS - Redis verification**
        You are currently trying to configure the channel `{channel}` for alerting purpose.
        Please use this token to confirm the setup: `{queue_name}`
        """
    ),
)

ALERT_DN_TEMPLATE = ChannelTemplate(
    RedisTemplate(
        """{date}: **Testing** The following domain name was updated: {dn}."""
    ),
)