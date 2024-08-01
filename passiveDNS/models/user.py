from enum import Enum

from Crypto.Protocol.KDF import bcrypt_check, bcrypt
from passiveDNS.models.meta_node import Node


class UserRole(Enum):
    ADMIN = "admin"
    USER = "user"
    SCHEDULER = "scheduler"


USER_COLLECTION = "Users"


class User(Node):
    def __init__(self, **user_json):
        """
        The User constructor
        :param user_json: the JSON parsed object as returned by `self.json()`
        """
        self.username = user_json["_key"]
        super().__init__(USER_COLLECTION, self.username)

        self.hashed_password = user_json["hashed_password"]
        self.role = user_json["role"]
        self.api_keys = user_json["api_keys"]

    def json(self) -> dict:
        """
        Serialize the User
        :return: JSON
        """
        return {
            "_key": self.username,
            "hashed_password": self.hashed_password,
            "role": self.role,
            "api_keys": self.api_keys,
        }

    def safe_json(self) -> dict:
        """
        Serialize the User without hashed password
        :return: JSON
        """
        return {
            "_key": self.username,
            "role": self.role,
        }

    def verify_password(self, password) -> bool:
        """
        Compare the input password to the hashed password
        :param password: the password to check
        :return: True if equal, False else
        """
        try:
            bcrypt_check(password, self.hashed_password.encode())
            return True
        except ValueError:
            return False

    def update_password(self, password):
        """
        Change the hashed password
        :param password: the new plain text password
        :return:
        """
        self.hashed_password = self._hash_password(password)
        self._update()

    def update_api_keys(self, api_name, api_key):
        """
        Add or replace an API key
        :param api_name: the name of the api
        :param api_key: the key associated to the api
        :return:
        """
        self.api_keys[api_name] = api_key
        self._update()

    def remove_api_key(self, api_name):
        """
        Remove an API key
        :param api_name: the name of the api
        :return:
        """
        del self.api_keys[api_name]
        self._replace()

    @staticmethod
    def new(username: str, password: str, is_scheduler=False, is_admin=False):
        """
        Build a new User object
        :param username: the User name
        :param password: the User plain text password
        :param email: the User email for _default channel
        :param is_scheduler: tells if it is a User for automated tasks
        :return: a new User object
        """
        hashed_password = User._hash_password(password)
        if is_admin:
            role = UserRole.ADMIN.value
        elif is_scheduler:
            role = UserRole.SCHEDULER.value
        else:
            role = UserRole.USER.value

        return User(
            _key=username,
            hashed_password=hashed_password,
            role=role,
            api_keys={},
        )

    @staticmethod
    def _hash_password(password: str) -> str:
        """
        Hash a plain text password with bcrypt
        :param password: the plain text password
        :return: the hashed password
        """
        return bcrypt(password, 14).decode()

    @staticmethod
    def get(username: str):
        """
        Get an existing User from its name
        :param username: the User ame
        :return: an existing User
        """
        u = User._get(USER_COLLECTION, username)
        return User(**u)

    @staticmethod
    def exists(username: str):
        """
        Check if a User exists from its name
        :param username: the User name
        :return: True if exists, False else
        """
        return User._exists(USER_COLLECTION, username)

    @staticmethod
    def list():
        """
        Fetch all User from DB
        :return: a list of User
        """
        user_list = User._list(USER_COLLECTION)
        return [User(**u) for u in user_list]
