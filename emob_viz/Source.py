import psycopg2

from emob_viz.exception.SourceException import SourceException


class Source:
    def __init__(self, database: str, user: str, password: str, host: str, port: int):
        """
        Set up a source with the given information
        :param database: Name of the database to connect to
        :param user: Name of the user to use
        :param password: Password for the user
        :param host: host of the database
        :param port: port to use
        """
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    @classmethod
    def with_defaults(cls, database: str, user: str, password: str):
        """
        Set up a source with the given information
        :param database: Name of the database to connect to
        :param user: Name of the user to use
        :param password: Password for the user
        :return: An instance with default host and port
        """
        return Source(database, user, password, "localhost", 5432)

    def get_connection(self):
        """
        Connect to the database with the known credentials
        :return: The established connection
        """
        try:
            return psycopg2.connect(
                database=self.database,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
            )
        except Exception as e:
            raise SourceException("Unable to establish connection to database.", e)
