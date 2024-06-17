from db.database import get_db, ObjectNotFound


class Node(object):
    """
    The base class for Node collection
    """

    def __init__(self, col, key):
        """
        The Node constructor
        :param col: the Node collection
        :param key: the Node _key
        """
        self._key = key
        self._collection = col

    def json(self) -> dict:
        """
        Format the Node
        :return: the JSON formatted Node
        """
        pass

    def insert(self):
        """
        Insert a Node into the collection
        :return:
        """
        # fixme not filtering user input...
        session = get_db()
        session.exec_aql(f"""
            INSERT {self.json()} INTO {self._collection}
        """)

    def delete(self):
        """
        Delete a Node from the collection
        :return:
        """
        session = get_db()
        session.exec_aql(
            f"""
            REMOVE @key IN {self._collection}
        """,
            bind_vars={"key": self._key},
        )

    def _update(self):
        """
        Update a node in the collection
        :return:
        """
        session = get_db()
        session.exec_aql(
            f"""
        FOR c IN {self._collection}
            FILTER c._key == @key
            UPDATE c WITH {self.json()} IN {self._collection}
        """,
            bind_vars={"key": self._key},
        )
    
    def _replace(self):
        """
        Update a node in the collection
        :return:
        """
        session = get_db()
        session.exec_aql(
            f"""
        REPLACE "{self._key}" WITH {self.json()} IN {self._collection}
        """
        )

    @staticmethod
    def _get(col: str, key) -> dict:
        """
        Get an existing Node
        :param col: the Node collection
        :param key: the Node _key
        :return: the existing Node
        """
        session = get_db()
        o = session.exec_aql(
            f"""
            RETURN DOCUMENT("{col}", @key)
        """,
            bind_vars=({"key": key}),
        )

        if o[0] is None:
            raise ObjectNotFound(f"object in {col} with key {key} not found")

        return o[0]

    @staticmethod
    def _get_from_key(col: str, key_name: str, key_value) -> dict:
        """
        Get an existing Node with a key field different than _key
        :param col: the Node collection
        :param key_name: the field name to use for filter
        :param key_value: the field value to use for filter
        :return: the existing Node
        """
        session = get_db()
        o = session.exec_aql(
            f"""
            FOR u IN {col}
                FILTER u.{key_name} == @key_value
                RETURN u
        """,
            bind_vars=({"key_value": key_value}),
        )

        if len(o) == 0:
            raise ObjectNotFound(
                f"object in {col} with key:value {key_name}:{key_value} not found"
            )

        return o[0]

    @staticmethod
    def _exists(col: str, value: str) -> bool:
        """
        Check if a Node exists
        :param col: the Node collection
        :param value: the Node _key value
        :return: True if the Node exists, False else
        """
        session = get_db()
        o = session.exec_aql(
            f"""
            RETURN DOCUMENT("{col}", @key)
        """,
            bind_vars={"key": value},
        )

        return o[0] is not None

    @staticmethod
    def _exists_from_key(col: str, key_name: str, key_value: str) -> bool:
        """
        Check if a Node exists, using a different field than _key
        :param col: the Node collection
        :param key_name: the field name to use for filter
        :param key_value: the field value to use for filter
        :return: True if the Node exists, False else
        """
        session = get_db()
        o = session.exec_aql(
            f"""
                    FOR u IN {col}
                        FILTER u.{key_name} == @key_value
                        RETURN u
                """,
            bind_vars=({"key_value": key_value}),
        )

        return len(o) != 0

    @staticmethod
    def _list(col: str) -> list:
        """
        List all the Node in a collection
        :param col: the Node collection
        :return: the list of existing Node
        """
        session = get_db()
        o = session.exec_aql(f"""
            FOR o IN {col}
                RETURN o
        """)

        return o
