from passiveDNS.utils.channels.templates import (
    ChannelTemplate,
    RedisTemplate,
)

TEST_TEMPLATE = ChannelTemplate(
    RedisTemplate("""{date}: **Testing** channel redis"""),
)

ALERT_DN_TEMPLATE = ChannelTemplate(
    RedisTemplate(
        """{
        {date}: {data}
        }"""
    ),
)
