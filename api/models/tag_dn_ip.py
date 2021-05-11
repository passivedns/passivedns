from models.meta_edge import Edge
from models.tag import TAG_COLLECTION
from models.domain_name import DOMAIN_NAME_COLLECTION
from models.ip_address import IP_ADDRESS_COLLECTION

TAG_DN_IP_COLLECTION = "TagDnIp"


class TagDnIP(Edge):
    def __init__(self, **e_json):
        """
        The TagDnIp constructor
        Edge that connect Tag to DomainName of IPAddress
        :param e_json: the JSON parsed object as returned by `self.json()`
        """
        super(TagDnIP, self).__init__(
            TAG_DN_IP_COLLECTION, e_json['_from'], e_json['_to']
        )

        self.tag = e_json['tag']
        self.object = e_json['object']
        self.type = e_json['type']

    def json(self):
        """
        Serialize the TagDnIp
        :return: JSON
        """
        return {
            "_from": self._from,
            "_to": self._to,
            "tag": self.tag,
            "object": self.object,
            "type": self.type
        }

    @staticmethod
    def new(tag, object_key, object_type):
        """
        Build a new TagDnIp object
        :param tag: the tag name
        :param object_key: the domain name/IP address to link
        :param object_type: DomainName/IPAddress
        :return: the build TagDnIp object
        """
        from_id = TagDnIP._get_id(TAG_COLLECTION, tag)
        to_id = TagDnIP._get_id(object_type, object_key)
        return TagDnIP(
            _from=from_id, _to=to_id,
            tag=tag, object=object_key, type=object_type
        )

    @staticmethod
    def get(tag, object_key, object_type):
        """
        Get an existing link between a tag and an object
        :param tag: the tag name
        :param object_key: the domain name/IP address
        :param object_type: DomainName/IPAddress
        :return: the existing link
        """
        tag_edge = TagDnIP._get(
            TAG_DN_IP_COLLECTION,
            TAG_COLLECTION, tag,
            object_type, object_key
        )
        return TagDnIP(**tag_edge)

    @staticmethod
    def exists(tag, object_key, object_type):
        """
        Check if a link exists between a tag and an object
        :param tag: the tag name
        :param object_key: the domain name/IP address
        :param object_type: DomainName/IPAddress
        :return: True if exists, False else
        """
        return TagDnIP._exists(
            TAG_DN_IP_COLLECTION,
            TAG_COLLECTION, tag,
            object_type, object_key
        )

    @staticmethod
    def list_tags_from_object(object_key, object_type):
        """
        List all links connected to a specific domain name/IP address
        :param object_key: the domain name/IP address
        :param object_type: DomainName/IPAddress
        :return: a list of connected TagDnIp object
        """
        tags_list_json = TagDnIP._list_from(
            TAG_DN_IP_COLLECTION,
            object_type, object_key
        )

        return [
            TagDnIP(**t) for t in tags_list_json
        ]

    @staticmethod
    def list_from_tag(tag_name):
        """
        List all links connected to a specific tag
        :param tag_name: the tag name
        :return: a list of connected TagDnIp object
        """
        tags_list_json = TagDnIP._list_to(
            TAG_DN_IP_COLLECTION,
            TAG_COLLECTION, tag_name
        )

        return [
            TagDnIP(**t) for t in tags_list_json
        ]
