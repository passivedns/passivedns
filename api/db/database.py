import os

from arango import ArangoClient
from flask import g

from utils import config


class ObjectNotFound(Exception):
    pass


class DatabaseSession(object):
    """
    The session to use when interacting with the Arango Database
    Needs the host of the DB and the database name to interact with
    The environment MUST store the credentials
    """
    def __init__(self, host, database_name):
        self._client = ArangoClient(host)

        username = config.g.ARANGO_USERNAME
        password = config.g.ARANGO_PASSWORD
        self._db = self._client.db(database_name, username, password)

    def exec_aql(self, aql, bind_vars=None) -> list:
        """
        Execute an AQL query through the session
        :param aql: the query
        :param bind_vars: the variables to bind with the query (with the words starting with `@`)
        :return: the parsed JSON results
        """
        if bind_vars is None:
            bind_vars = {}

        cursor = self._db.aql.execute(aql, bind_vars=bind_vars)
        return [o for o in cursor]


def get_db():
    """
    Manage the session into the Flask application context
    :return: the DatabaseSession object
    """
    if 'db' not in g:
        db_host = config.g.DB_HOST
        g.db = DatabaseSession(db_host, "passive_dns")

    return g.db
