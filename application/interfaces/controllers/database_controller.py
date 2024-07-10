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


    def save_task(self, title, descript, deadline, user_id):
        """
        :param av:
        :param report:
        :param user:
        :return: bool depend on if insert is working
        """
        self.db_presenter.connect()
        result = self.db_presenter.execute_command(
            f"INSERT INTO TASKS(title, descript, deadline, user_id) "
            f"VALUES ('{title}', '{descript}', '{deadline}', '{user_id}')"
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