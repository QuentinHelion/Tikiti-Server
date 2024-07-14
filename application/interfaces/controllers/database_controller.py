"""
Database controller
"""

from application.interfaces.presenters.database_presenter import DatabasePresenter


class DatabaseController:
    """
    Database controller
    """

    def __init__(self, host, user, password, database):
        self.db_presenter = DatabasePresenter(
            host=host,
            database=database,
            user=user,
            password=password
        )

    def insert(self, table, columns, values):
        """
        :param table: table 
        :param columns: table's columns
        :param values: column's values
        :return: bool depend on if insert is working
        """
        self.db_presenter.connect()
        delimiter = ','
        if isinstance(columns, list):
            columns = delimiter.join(map(str, columns))

        if isinstance(values, list):
            values = delimiter.join([f"'{str(v)}'" for v in values])

        result = self.db_presenter.execute_command(
            f"INSERT INTO {table}({columns}) "
            f"VALUES ({values})"
        )

        self.db_presenter.disconnect()
        return result

    def select(self, table, select="*", columns=None, values=None):
        """
        Select raw from table
        :return: string
        """
        self.db_presenter.connect()

        if columns is not None and values is not None:
            if isinstance(columns, list):
                if isinstance(values, list):
                    if len(values) == len(columns):
                        condition = f"{columns[0]} = '{values[0]}'"
                        for i in range(1, len(columns)):
                            condition += f" AND {columns[i]} = '{values[i]}'"
            else:
                condition = f"{columns} = '{values}'"
        else:
            condition = ""

        result = self.db_presenter.execute_query(
            f"SELECT {select} FROM {table} "
            f"WHERE {condition}"
        )

        self.db_presenter.disconnect()
        return result

    def delete(self, table, columns=None, values=None):
        """
        delete raw from table
        :return: string
        """
        self.db_presenter.connect()

        if columns is not None and values is not None:
            if isinstance(columns, list):
                if isinstance(values, list):
                    if len(values) == len(columns):
                        condition = f"{columns[0]} = '{values[0]}'"
                        for i in range(1, len(columns)):
                            condition += f" AND {columns[i]} = '{values[i]}'"
            else:
                condition = f"{columns} = '{values}'"
        else:
            return False

        result = self.db_presenter.execute_command(
            f"DELETE FROM {table} "
            f"WHERE {condition}"
        )
        self.db_presenter.connect()
        return result

    def update(self, table, columns=None, values=None, condition=None):
        """
        Update raw from table
        :param table: table
        :param columns: table's columns
        :param values: column's values
        :param condition: condition
        :return: bool depend on if update is working
        """
        self.db_presenter.connect()
        if columns is not None and values is not None:
            if isinstance(columns, list):
                if isinstance(values, list):
                    if len(values) == len(columns):
                        sets = f"{columns[0]} = '{values[0]}'"
                        for i in range(1, len(columns)):
                            sets += f" AND {columns[i]} = '{values[i]}'"
            else:
                sets = f"{columns} = '{values}'"
        else:
            return False

        print(
            f"UPDATE {table} "
            f"SET {sets} "
            f"WHERE {condition}"
        )

        result = self.db_presenter.execute_command(
            f"UPDATE {table} "
            f"SET {sets} "
            f"WHERE {condition}"
        )

        self.db_presenter.connect()
        return result
