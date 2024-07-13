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

        print("check if user exist")
        print(user_id)
        print(self.db_controller.select(
            table="USERS",
            select="id",
            columns="id",
            values=user_id
        ))

        if len(self.db_controller.select(
                table="USERS",
                columns="id",
                values=user_id
        )) == 0: return False

        print("insert new task")
        return self.db_controller.insert(
            table="TASKS",
            columns=["title", "user_id", "deadline", "descript"],
            values=[title, user_id, deadline, descript if descript is not None else ""]
        )
