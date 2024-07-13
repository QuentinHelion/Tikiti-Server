"""
This file contain most task methods
"""


class TaskManager:
    """
    Class with all methods
    """

    def __init__(self, db_controller):
        self.db_controller = db_controller

    def new(self, title, user_id, deadline, descript=None):
        """
        Methods to create new task
        :param title: Task's title
        :param user_id: ID of task's owner
        :param deadline: Task's deadline
        :param descript: Task's description (optional)
        :return: bool, depend on result of task saving
        """

        if len(self.db_controller.select(
                table="USERS",
                columns="id",
                values=user_id
        )) == 0: return False

        return self.db_controller.insert(
            table="TASKS",
            columns=["title", "user_id", "deadline", "descript"],
            values=[title, user_id, deadline, descript if descript is not None else ""]
        )

    def delete(self, id):
        """
        Methods to delete task
        :param id: ID of task
        :return: bool, depend on result of task deletion
        """
        return self.db_controller.delete(
            table="TASKS",
            columns="id",
            value=id
        )
