from arango import ArangoClient
from arango.exceptions import GraphCreateError

import logging
import requests
import time
import sys
import yaml

from passiveDNS.utils import config


class ObjectNotFound(Exception):
    pass


class DatabaseSession(object):
    """
    The session to use when interacting with the Arango Database
    Needs the host of the DB and the database name to interact with
    The environment MUST store the credentials
    """

    def __init__(self):
        self._client = None
        self._db = None
        self.collections = dict()
        self.graphs = dict()

    def connect(
        self,
        host: str = None,
        # port: str = None,
        username: str = None,
        password: str = None,
        database_name: str = None,
    ):
        if config.g is None:
            config.init_config()

        host = host or config.g.DB_HOST
        # port = port or config.g.DB_PORT
        username = username or config.g.ARANGO_USERNAME
        password = password or config.g.ARANGO_PASSWORD
        database = database_name or config.g.DB_NAME

        # host_string = f"http://{host}:{port}"

        self._client = ArangoClient(host)

        # connect to system
        self._sys_db = self._client.db("_system", username=username, password=password)

        for _ in range(0, 4):
            try:
                self._db = self._sys_db.has_database(database)
                break
            except requests.exceptions.ConnectionError as e:
                logging.error("Connection error: {0:s}".format(str(e)))
                logging.error("Retrying in 5 seconds...")
                time.sleep(5)
        else:
            logging.error("Could not connect, bailing.")
            sys.exit(1)

        # check
        if not self._db:
            self._sys_db.create_database(database)

        self._db = self._client.db(database, username=username, password=password)
        # add graph database

        # create edges and nodes associated
        self.create_edge_definition(
            self.graph("passive_dns"),
            {
                "edge_collection": "UsersDn",
                "from_vertex_collections": ["Users"],
                "to_vertex_collections": ["DomainName"],
            },
        )

        self.create_edge_definition(
            self.graph("passive_dns"),
            {
                "edge_collection": "UsersChannel",
                "from_vertex_collections": ["Users"],
                "to_vertex_collections": ["Channel"],
            },
        )

        self.create_edge_definition(
            self.graph("passive_dns"),
            {
                "edge_collection": "DomainNameResolution",
                "from_vertex_collections": ["DomainName"],
                "to_vertex_collections": ["IPAddress"],
            },
        )

        self.create_edge_definition(
            self.graph("passive_dns"),
            {
                "edge_collection": "TagDnIp",
                "from_vertex_collections": ["Tag"],
                "to_vertex_collections": ["DomainName", "IPAddress"],
            },
        )

        # create alone nodes
        self.collection("UsersRequest")
        self.collection("UsersPending")
        extern_api_collection = self.collection("APIIntegration")

        # add extern apis data
        file_path = "passiveDNS/db/extern_apis.yml"

        with open(file_path, 'r') as file:
            extern_apis = list(yaml.safe_load_all(file))
        
        for api in extern_apis:
            if not extern_api_collection.has(api["_key"]):
                extern_api_collection.insert(api)


        # empty default channel
        if not self._db.collection("Channel").has("_default"):
            self._db.collection("Channel").insert(
                {
                    "_key": "_default",
                    "type": "email",
                    "infos": {
                        "smtp_host": "",
                        "smtp_port": "",
                        "sender_email": "",
                        "sender_password": "",
                    },
                }
            )

        return

    def clear(self, truncate=True):
        if not self._db:
            self.connect()
        for collection_data in self._db.collections():
            if collection_data["system"]:
                continue
            if truncate:
                collection = self._db.collection(collection_data["name"])
                collection.truncate()
            else:
                self._db.delete_collection(collection_data["name"])
        self.collections = {}

    # create or get collection
    def collection(self, name):
        if self._db is None:
            self.connect()

        if name not in self.collections:
            if self._db.has_collection(name):
                self.collections[name] = self._db.collection(name)
            else:
                self.collections[name] = self._db.create_collection(name)

        return self.collections[name]

    # create graph
    def graph(self, name):
        if self._db is None:
            self.connect()

        try:
            return self._db.create_graph(name)
        except GraphCreateError as err:
            if err.error_code in [1207, 1925]:
                return self._db.graph(name)
            raise

    # create or get edge
    def create_edge_definition(self, graph, definition):
        if self._db is None:
            self.connect()

        if not self._db.has_collection(definition["edge_collection"]):
            collection = graph.create_edge_definition(**definition)
        else:
            collection = self._db.collection(definition["edge_collection"])

        self.collections[definition["edge_collection"]] = collection
        return collection

    def exec_aql(self, aql, bind_vars=None) -> list:
        """
        Execute an AQL query through the session
        :param aql: the query
        :param bind_vars: the variables to bind with the query (with the words starting with `@`)
        :return: the parsed JSON results
        """

        if self._db is None:
            self.connect()

        if bind_vars is None:
            bind_vars = {}

        cursor = self._db.aql.execute(aql, bind_vars=bind_vars)
        return [o for o in cursor]


def get_db():
    """
    Manage the session into the FastAPI application context
    :return: the DatabaseSession object
    """
    return DatabaseSession()
