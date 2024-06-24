from passiveDNS.channels.templates import (
    ChannelTemplate,
    EmailTemplate,
    TelegramTemplate,
    PARSE_MODE_MARKDOWN,
    DiscordTemplate,
)

TEST_TEMPLATE = ChannelTemplate(
    EmailTemplate(
        "Passive DNS Testing",
        """
        {date}: <b>Testing</b> channel email...
        """,
    ),
    TelegramTemplate(
        """
        {date}: *Testing* channel telegram...
        """,
        PARSE_MODE_MARKDOWN,
    ),
    DiscordTemplate(
        """
        {date}: **Testing** channel discord
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
    TelegramTemplate(
        """
        You have been invited by the admin of Passive DNS to join in, as a user.
        Use this token to register on the server: {token} 
    
        Cheers,
        """,
        PARSE_MODE_MARKDOWN,
    ),
    DiscordTemplate(
        """
        You have been invited by the admin of Passive DNS to join in, as a user.
        Use this token to register on the server: {token} 
    
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
    TelegramTemplate(
        """
        *Passive DNS - telegram verification*
    
You are currently trying to configure the channel `{channel}` for alerting purpose.

Please use this token to confirm the setup: `{token}`
            
        Cheers,
    """,
        PARSE_MODE_MARKDOWN,
    ),
    DiscordTemplate(
        """
        **Passive DNS - Discord verification**
        You are currently trying to configure the channel `{channel}` for alerting purpose.
        Please use this token to confirm the setup: `{token}`
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
    TelegramTemplate(
        """
*Passive DNS alert*

You can find the whole list and export it at this URL: {url_alerts}.

```{table}```

NB: you are receiving this alert via Telegram because you configured it in the Passive DNS application.
To unsubscribe from those alerts, please remove this channel from your settings: {url_channels}.
        """,
        PARSE_MODE_MARKDOWN,
    ),
    DiscordTemplate(
        """
**Passive DNS alert**

You can find the whole list and export it at this URL: {url_alerts}.

```{table}```

NB: you are receiving this alert via Discord because you configured it in the Passive DNS application.
To unsubscribe from those alerts, please remove this channel from your settings: {url_channels}.
        """
    ),
)
