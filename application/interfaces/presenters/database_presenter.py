"""
Database usage presenter
"""

import mysql.connector


class DatabasePresenter:
    """
    Gateway to db
    """

    def __init__(self, host, database, user, password, port=3306):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.connection = None
        print("DB presenter OK")

    def connect(self):
        """
        Connection to db
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
                auth_plugin='mysql_native_password'
            )
            print("Database connection ok")
        except mysql.connector.Error as error:
            print(f"Error connecting to MySQL: {error}")

    def disconnect(self):
        """
        Disconnect from db
        """
        self.connection.close()

    def execute_query(self, query):
        """
        Execute SQL query on db
        :param query: sql command
        :return: result
        """
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def execute_command(self, query):
        """
        Execute SQL command on db
        :param query: sql command
        :return: bool
        """
        cursor = self.connection.cursor()
        try:
            cursor.execute(query)
            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False
        finally:
            cursor.close()