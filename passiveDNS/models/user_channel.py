from models.meta_edge import Edge
from models.user import USER_COLLECTION
from models.channel import CHANNEL_COLLECTION
import secrets

USER_CHANNEL_COLLECTION = "UsersChannel"


class UserChannel(Edge):
    def __init__(self, **e_json):
        """
        The User channel constructor
        :param e_json: the JSON parsed object as returned by `self.json()`
        """
        super().__init__(
            USER_CHANNEL_COLLECTION,
            e_json['_from'],
            e_json['_to']
        )
        self.username = e_json['username']
        self.channel_name = e_json['channel_name']
        self.contact = e_json['contact']
        self.verified = e_json['verified']
        self.token = e_json['token']

    def json(self):
        """
        Serialize the User channel
        :return: JSON
        """
        return {
            "_from": self._from,
            "_to": self._to,
            "username": self.username,
            "channel_name": self.channel_name,
            "contact": self.contact,
            "verified": self.verified,
            "token": self.token
        }

    def safe_json(self):
        """
        Serialize the User channel without private infos
        :return: JSON
        """
        return {
            "channel_name": self.channel_name,
            "contact": self.contact,
            "verified": self.verified
        }

    def update(self, verified):
        """
        Set a User channel as verified
        :param verified: The verified value (bool)
        :return:
        """
        self.verified = verified
        self._update(dict(
            verified=verified
        ))

    @staticmethod
    def new(username, channel_name, contact):
        """
        Build a new User channel object
        :param username: the User name
        :param channel_name: the Channel name
        :param contact: the User contact
        :return: a new User channel object
        """
        from_id = UserChannel._get_id(USER_COLLECTION, username)
        to_id = UserChannel._get_id(CHANNEL_COLLECTION, channel_name)
        token = secrets.token_hex(16)
        return UserChannel(
            _from=from_id,
            _to=to_id,
            username=username,
            channel_name=channel_name,
            contact=contact,
            verified=False,
            token=token
        )

    @staticmethod
    def exists(username: str, channel_name: str):
        """
        Check if a User channel exists
        :param username: the User name
        :param channel_name: the Channel name
        :return: an existing User channel name
        """
        return UserChannel._exists(
            USER_CHANNEL_COLLECTION,
            USER_COLLECTION, username,
            CHANNEL_COLLECTION, channel_name
        )

    @staticmethod
    def get(username: str, channel_name: str):
        """
        Get an existing User channel
        :param username: the User name
        :param channel_name: the Channel name
        :return: an existing User channel
        """
        u_ch = UserChannel._get(
            USER_CHANNEL_COLLECTION,
            USER_COLLECTION, username,
            CHANNEL_COLLECTION, channel_name
        )
        return UserChannel(**u_ch)

    @staticmethod
    def list_from_username(username: str):
        """
        List all User channels with a specific User name
        :param username: the User name
        :return: a list of User channel
        """
        edges = UserChannel._list_to(
            USER_CHANNEL_COLLECTION,
            USER_COLLECTION, username
        )
        return [
            UserChannel(**e) for e in edges
        ]

    @staticmethod
    def list_from_channel(channel: str):
        """
        List all User channel connecting a specific Channel
        :param channel: the Channel name
        :return: a list of User channel
        """
        edges = UserChannel._list_from(
            USER_CHANNEL_COLLECTION,
            CHANNEL_COLLECTION, channel
        )

        return [
            UserChannel(**e) for e in edges
        ]
