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

    def select(self, table, select="*", columns=None, values=None, custom_condition=""):
        """
        Get all tasks from user id
        :return: string
        """
        self.db_presenter.connect()

        if columns is not None and values is not None:
            if isinstance(columns, list):
                if isinstance(values, list):
                    if len(values) == len(columns):
                        condition = f"{columns[0]} = '{values[0]}'"
                        # condition.join([f" AND {columns[i]} = '{values[i]}'" for i in range(1, len(columns))])
                        for i in range(1, len(columns)):
                            condition += f" AND {columns[i]} = '{values[i]}'"
            else:
                condition = f"{columns} = '{values}'"
        else:
            condition = ""


        result = self.db_presenter.execute_query(
                f"SELECT {select} FROM {table} "
                f"WHERE {condition} {custom_condition}"
            )

        self.db_presenter.disconnect()
        return result
