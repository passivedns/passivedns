class ChannelMeta(object):
    """
    The base class for Channel settings
    Parse the settings according to the Channel type
    """

    def __init__(self, infos_json, attributes):
        self._attributes = attributes

        for a in self._attributes:
            self.__setattr__(a, infos_json[a])

    def json(self):
        out = dict()
        for a in self._attributes:
            out[a] = self.__getattribute__(a)

        return out


class ChannelTelegram(ChannelMeta):
    TYPE = "telegram"

    def __init__(self, **infos_json):
        super().__init__(infos_json, ["bot_token"])


class ChannelEmail(ChannelMeta):
    TYPE = "email"

    def __init__(self, **infos_json):
        super().__init__(
            infos_json, ["smtp_host", "smtp_port", "sender_email", "sender_password"]
        )


class ChannelDiscord(ChannelMeta):
    TYPE = "discord"

    def __init__(self, **infos_json):
        super().__init__(infos_json, ["bot_token"])


class ChannelRedis(ChannelMeta):
    TYPE = "redis"

    def __init__(self, **infos_json):
        super().__init__(infos_json, ["host", "port", "db", "queue_name", "password"])
