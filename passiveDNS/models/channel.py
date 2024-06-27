from passiveDNS.models.channel_meta import ChannelTelegram, ChannelEmail, ChannelDiscord
from passiveDNS.models.meta_node import Node

CHANNEL_COLLECTION = "Channel"


class ChannelTypeError(Exception):
    pass


class Channel(Node):
    DEFAULT = "_default"

    def __init__(self, **ch_json):
        """
        The Channel constructor
        :param ch_json: the JSON parsed object as returned by `self.json()`
        """

        self.name = ch_json["_key"]
        self.type = ch_json["type"]
        super().__init__(CHANNEL_COLLECTION, self.name)

        infos = ch_json["infos"]
        self._parse_infos(infos)

    # ===== DB stuff =====
    def _parse_infos(self, infos):
        """
        Parse the channel settings according to the channel type
        :param infos: the settings
        :return:
        :raise: ChannelTypeError if type cannot be parsed
        """

        if self.type == ChannelEmail.TYPE:
            self.infos = ChannelEmail(**infos)

        elif self.type == ChannelTelegram.TYPE:
            self.infos = ChannelTelegram(**infos)

        elif self.type == ChannelDiscord.TYPE:
            self.infos = ChannelDiscord(**infos)

        else:
            raise ChannelTypeError(f"cannot parse channel of type {self.type}")

    def json(self):
        """
        Serialize the Channel
        :return: JSON
        """
        return {"_key": self.name, "type": self.type, "infos": self.infos.json()}

    def safe_json(self):
        """
        Serialize the Channel without sensitive settings
        :return: JSON
        """
        return {"_key": self.name, "type": self.type}

    def update(self, infos):
        """
        Update the channel with new settings
        :param infos: the new settings
        :return:
        """
        self._parse_infos(infos)
        self._update()

    # ===== static stuff =====
    @staticmethod
    def new(name: str, ch_type: str, infos: dict):
        """
        Build a new Channel object
        :param name: the Channel name
        :param ch_type: the Channel type
        :param infos: the Channel settings
        :return: a new Channel object
        """
        return Channel(_key=name, type=ch_type, infos=infos)

    @staticmethod
    def get(name):
        """
        Get an existing Channel from its name
        :param name: the requested Channel name
        :return: the requested Channel object
        :raise: ObjectNotFound if not found
        """
        ch = Channel._get(CHANNEL_COLLECTION, name)
        return Channel(**ch)

    @staticmethod
    def exists(name):
        """
        Check if a Channel exists from its name
        :param name: the requested Channel name
        :return: True if exists, False else
        """
        return Channel._exists(CHANNEL_COLLECTION, name)

    @staticmethod
    def list():
        """
        List all stored Channels
        :return: a list of Channel objects
        """
        ch_list = Channel._list(CHANNEL_COLLECTION)
        return [Channel(**ch) for ch in ch_list]
