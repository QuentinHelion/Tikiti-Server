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

    def get_tasks(self, user_id):
        """
        Get all tasks from user id
        :return: string
        """
        self.db_presenter.connect()
        result = self.db_presenter.execute_command(
                f"SELECT * FROM TASKS WHERE "
                f"user_id LIKE {user_id}')"
            )
        self.db_presenter.disconnect()
        return result