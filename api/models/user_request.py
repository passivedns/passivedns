from datetime import datetime

from models.meta_node import Node

USER_REQUEST_COLLECTION = "UsersRequest"


class UserRequest(Node):
    def __init__(self, **user_request_json):
        """
        The User request constructor
        :param user_request_json: the JSON parsed object as returned by `self.json()`
        """
        self.email = user_request_json['_key']
        super().__init__(USER_REQUEST_COLLECTION, self.email)

        self.requested_at = datetime.fromisoformat(
            user_request_json['requested_at']
        )

    def json(self) -> dict:
        """
        Serialize the User request
        :return: JSON
        """
        return {
            '_key': self.email,
            'requested_at': self.requested_at.isoformat()
        }

    @staticmethod
    def new(email: str):
        """
        Build a new User request
        :param email: the User email
        :return: a new User request
        """
        requested_at = datetime.now().isoformat()
        return UserRequest(_key=email, requested_at=requested_at)

    @staticmethod
    def get(email):
        """
        Get an existing User request from its email
        :param email: the User email
        :return: an existing User request
        """
        ur = UserRequest._get(USER_REQUEST_COLLECTION, email)
        return UserRequest(**ur)

    @staticmethod
    def exists(email):
        """
        Check of a User request exists from its email
        :param email: the User email
        :return: True if exists, False else
        """
        return UserRequest._exists(USER_REQUEST_COLLECTION, email)

    @staticmethod
    def list():
        """
        List all User request
        :return: a list of User request
        """
        ur_list = UserRequest._list(USER_REQUEST_COLLECTION)
        return [
            UserRequest(**u) for u in ur_list
        ]
