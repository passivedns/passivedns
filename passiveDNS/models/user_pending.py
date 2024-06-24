import secrets
from datetime import datetime

from passiveDNS.models.meta_node import Node
from passiveDNS.utils import timezone, config

USER_PENDING_COLLECTION = "UsersPending"


class UserPending(Node):
    def __init__(self, **user_pending_json):
        """
        The User pending constructor
        :param user_pending_json: the JSON parsed object as returned by `self.json()`
        """
        self.token = user_pending_json["_key"]
        super().__init__(USER_PENDING_COLLECTION, self.token)

        self.email = user_pending_json["email"]
        self.invited_at = datetime.fromisoformat(user_pending_json["invited_at"])

    def json(self) -> dict:
        """
        Serialize the User pending
        :return: JSON
        """
        return {
            "_key": self.token,
            "email": self.email,
            "invited_at": self.invited_at.isoformat(),
        }

    def safe_json(self) -> dict:
        """
        Serialize the User pending without the verification token
        :return: JSON
        """
        return {"email": self.email, "invited_at": self.invited_at.isoformat()}

    @staticmethod
    def new(email: str):
        """
        Build a new User pending
        :param email: the User email
        :return: a new User pending
        """
        token = secrets.token_hex(16)
        invited_at = timezone.get_current_datetime(config.g.TIMEZONE)

        return UserPending(_key=token, email=email, invited_at=invited_at)

    @staticmethod
    def get(token: str):
        """
        Get an existing User pending from a verification token
        :param token: the verification token
        :return: an existing User pending
        """
        up = UserPending._get(USER_PENDING_COLLECTION, token)
        return UserPending(**up)

    @staticmethod
    def exists(token: str) -> bool:
        """
        Check if a User pending exists from its token
        :param token: the verification token
        :return: an existing User pending
        """
        return UserPending._exists(USER_PENDING_COLLECTION, token)

    @staticmethod
    def exists_from_email(email: str):
        """
        Check if a User pending exists from the User email
        :param email: the User email
        :return: an existing User pending
        """
        return UserPending._exists_from_key(USER_PENDING_COLLECTION, "email", email)

    @staticmethod
    def list():
        """
        List all the existing User pending
        :return: a list of User pending
        """
        up_list = UserPending._list(USER_PENDING_COLLECTION)
        return [UserPending(**u) for u in up_list]
