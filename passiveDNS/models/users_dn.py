from passiveDNS.models.meta_edge import Edge
from passiveDNS.models.user import USER_COLLECTION
from passiveDNS.models.domain_name import DOMAIN_NAME_COLLECTION

USER_DN_COLLECTION = "UsersDn"


class UserDn(Edge):
    def __init__(self, **e_json):
        """
        The User DN constructor
        :param e_json: the JSON parsed object as returned by `self.json()`
        """
        super().__init__(USER_DN_COLLECTION, e_json["_from"], e_json["_to"])

        self.username = e_json["username"]
        self.domain_name = e_json["domain_name"]
        self.owned = e_json["owned"]

    def json(self):
        """
        Serialize the User DN object
        :return: JSON
        """
        return {
            "_from": self._from,
            "_to": self._to,
            "username": self.username,
            "domain_name": self.domain_name,
            "owned": self.owned,
        }

    @staticmethod
    def new(username, domain_name, owned):
        """
        Build a new User DN Object
        :param owned: True if created by the User, False else
        :param username: the User name
        :param domain_name: the DomainName name
        :return: a new User DN link
        """
        from_id = UserDn._get_id(USER_COLLECTION, username)
        to_id = UserDn._get_id(DOMAIN_NAME_COLLECTION, domain_name)
        return UserDn(
            _from=from_id,
            _to=to_id,
            username=username,
            domain_name=domain_name,
            owned=owned,
        )

    @staticmethod
    def get(username, domain_name):
        """
        Get an existing User DN
        :param username: the User name
        :param domain_name: the domain name
        :return: an existing User DN
        """
        user_dn = UserDn._get(
            USER_DN_COLLECTION,
            USER_COLLECTION,
            username,
            DOMAIN_NAME_COLLECTION,
            domain_name,
        )
        return UserDn(**user_dn)

    @staticmethod
    def exists(username, domain_name) -> bool:
        """
        Check if a User DN exists
        :param username: the User name
        :param domain_name: the domain name
        :return: True if exists, False else
        """
        return UserDn._exists(
            USER_DN_COLLECTION,
            USER_COLLECTION,
            username,
            DOMAIN_NAME_COLLECTION,
            domain_name,
        )

    @staticmethod
    def list_dn_from_user(username):
        """
        List all User DN connection a specific User
        :param username: the User name
        :return: all User DN connected
        """
        user_dn_list = UserDn._list_to(USER_DN_COLLECTION, USER_COLLECTION, username)
        return [UserDn(**user_dn) for user_dn in user_dn_list]
    
    @staticmethod
    def list_user_from_dn(domain_name):
        """
        List all User DN connection a specific DomainName
        :param domain_name: the Domain name
        :return: all User DN connected
        """
        user_dn_list = UserDn._list_from(USER_DN_COLLECTION, DOMAIN_NAME_COLLECTION, domain_name)
        return [UserDn(**user_dn) for user_dn in user_dn_list]
