from passiveDNS.utils.channels.templates import (
    ChannelTemplate,
    EmailTemplate,
    RedisTemplate,
)

TEST_TEMPLATE = ChannelTemplate(
    EmailTemplate(
        "Passive DNS Testing",
        """
        {date}: <b>Testing</b> channel email...
        """,
    ),
    RedisTemplate(
        """
        {date}: **Testing** channel redis
        """
    ),
)

INVITE_TEMPLATE = ChannelTemplate(
    EmailTemplate(
        "Passive DNS invitation",
        """
        You have been invited by the admin of Passive DNS to join in, as a user.
        Use this token to register on the server: {token} 
    
        Cheers,
        """,
    ),
    RedisTemplate(
        """
        You have been invited by the admin of Passive DNS to join in, as a user.
        Cheers,
        """
    ),
)

CHANNEL_VERIFY_TEMPLATE = ChannelTemplate(
    EmailTemplate(
        "Passive DNS - email verification",
        """
        You are currently trying to configure the channel {channel} for alerting purpose.    
        Please use this token to confirm the setup: {token}
        
        Cheers,
        """,
    ),
    RedisTemplate(
        """
        **Passive DNS - Redis verification**
        You are currently trying to configure the channel `{channel}` for alerting purpose.
        Please use this token to confirm the setup: `{queue_name}`
        """
    ),
)

ALERT_LIST_TEMPLATE = ChannelTemplate(
    EmailTemplate(
        "Passive DNS Alert",
        """
Please find below the list of recently updated Domain Names.

You can find the whole list and export it at this URL: {url_alerts}.

<pre>{table}</pre>

NB: you are receiving this email because you configured it in the Passive DNS application.
To unsubscribe from those alerts, please remove this channel from your settings: {url_channels}.
        """,
    ),
    RedisTemplate(
        """
        {date}: **Testing** channel redis
        """
    ),
)
