from models.meta_node import Node

TAG_COLLECTION = "Tag"


class Tag(Node):
    def __init__(self, **tag_json):
        """
        the Tag constructor
        :param tag_json: the JSON parsed object as returned by `self.json()`
        """
        self.name = tag_json['_key']
        super(Tag, self).__init__(TAG_COLLECTION, self.name)

    def json(self):
        """
        Serialize the Tag
        :return: JSON
        """
        return {
            "_key": self.name
        }

    @staticmethod
    def new(name):
        """
        Build a new Tag
        :param name: the tag name
        :return: the Tag object
        """
        return Tag(_key=name)

    @staticmethod
    def get(name):
        """
        Get an existing Tag from its name
        :param name: the tag name
        :return: the Tag object
        """
        tag_json = Tag._get(TAG_COLLECTION, name)
        return Tag(**tag_json)

    @staticmethod
    def exists(name):
        """
        Check if a Tag exists from its name
        :param name: the tag name
        :return: True if exists, False else
        """
        return Tag._exists(TAG_COLLECTION, name)

    @staticmethod
    def list():
        """
        List all Tag object
        :return: the list of Tag object
        """
        tag_json_list = Tag._list(TAG_COLLECTION)
        return [
            Tag(**j) for j in tag_json_list
        ]
