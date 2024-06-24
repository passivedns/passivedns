from passiveDNS.db.database import get_db, ObjectNotFound


class Edge(object):
    """
    The base class for Edge collections
    """

    def __init__(self, col, _from, _to):
        """
        The Edge constructor
        :param col: the edge collection
        :param _from: the _from ID
        :param _to: the _to ID
        """
        self._from = _from
        self._to = _to
        self._collection = col

    def json(self) -> dict:
        """
        Format the Edge
        :return: the JSON formatted Edge
        """
        pass

    def insert(self):
        """
        Insert an Edge into the collection
        :return:
        """
        # fixme not filtering user input...
        session = get_db()
        session.exec_aql(f"""
            INSERT {self.json()} INTO {self._collection}
        """)

    def delete(self):
        """
        Delete an Edge from the collection
        :return:
        """
        session = get_db()
        session.exec_aql(
            f"""
        FOR o IN {self._collection}
            FILTER o._from == @from AND o._to == @to
            REMOVE o IN {self._collection}
        """,
            bind_vars={"from": self._from, "to": self._to},
        )

    def _update(self, values: dict):
        """
        Update an Edge from the collection
        :param values: the value to update
        :return:
        """
        session = get_db()
        session.exec_aql(
            f"""
        FOR o IN {self._collection}
            FILTER o._from == @from AND o._to == @to
            UPDATE o WITH {values} IN {self._collection} 
        """,
            bind_vars={"from": self._from, "to": self._to},
        )

    @staticmethod
    def _get_id(col: str, key: str):
        """
        Build an ID from the object _key and the object collection
        :param col: the object collection
        :param key: the object _key
        :return: the build ID
        """
        return f"{col}/{key}"

    @staticmethod
    def _get(col: str, col_from: str, _from: str, col_to: str, _to: str) -> dict:
        """
        Get an existing Edge
        :param col: the Edge collection
        :param col_from: the _from collection
        :param _from: the _from _key
        :param col_to: the _to collection
        :param _to: the _to key
        :return: the existing Edge
        """
        _from_id = Edge._get_id(col_from, _from)
        _to_id = Edge._get_id(col_to, _to)

        session = get_db()
        o = session.exec_aql(
            f"""
        FOR o IN {col}
            FILTER o._from == @from AND o._to == @to
            RETURN o
        """,
            bind_vars={"from": _from_id, "to": _to_id},
        )

        if len(o) == 0:
            raise ObjectNotFound(
                f"object in {col} with _from {_from_id}" f" and _to {_to_id} not found"
            )

        return o[0]

    @staticmethod
    def _exists(col: str, col_from: str, _from: str, col_to: str, _to: str) -> bool:
        """
        Check if an Edge exists
        :param col: the Edge collection
        :param col_from: the _from collection
        :param _from: the _from _key
        :param col_to: the _to collection
        :param _to: the _to key
        :return: True if the Edge exits, False else
        """
        _from_id = Edge._get_id(col_from, _from)
        _to_id = Edge._get_id(col_to, _to)

        session = get_db()
        o = session.exec_aql(
            f"""
        FOR o IN {col}
            FILTER o._from == @from AND o._to == @to
            RETURN o
        """,
            bind_vars={"from": _from_id, "to": _to_id},
        )

        return len(o) != 0

    @staticmethod
    def _list(col: str) -> list:
        """
        List all the Edge
        :param col: the Edge collection
        :return: the Edge parsed list
        """
        session = get_db()
        o = session.exec_aql(f"""
        FOR o IN {col}
            RETURN o
        """)

        return o

    @staticmethod
    def _list_from(col: str, col_to: str, _to: str):
        """
        List all the Edge connected to the object _to
        :param col: the Edge collection
        :param col_to: the _to collection
        :param _to: the _to _key
        :return: the list of connected Edge
        """
        _to_id = Edge._get_id(col_to, _to)

        session = get_db()
        o = session.exec_aql(
            f"""
        FOR o IN {col}
            FILTER o._to == @to
            RETURN o
        """,
            bind_vars={"to": _to_id},
        )

        return o

    @staticmethod
    def _list_to(col: str, col_from: str, _from: str):
        """
        List all the Edge connected to the object _from
        :param col: the Edge collection
        :param col_from: the _from collection
        :param _from: the _from _Key
        :return: the list of connected Edge
        """
        _from_id = Edge._get_id(col_from, _from)

        session = get_db()
        o = session.exec_aql(
            f"""
        FOR o IN {col}
            FILTER o._from == @from
            RETURN o
        """,
            bind_vars={"from": _from_id},
        )

        return o
