"""
This file contain most of task mathods
"""

class TaskManager:
    """
    Class with all methoods
    """

    def __ini__(self, db_controller):
        self.db_controller = db_controller

    
    def new(self, title, user_id, deadline, descript=None):
        """
        Methods to create new task
        :param title: Task's title
        :param user_id: ID of task's owner
        :param deadline: Task's deadline
        :param desc: Task's description (optionnal)
        :return: bool, depend of result of task saving
        """

        if not self.db_controller.select(
            table="USERS",
            columns="id",
            values=user_id
        ): return False

        return self.db_controller.insert(
            table="TASKS",
            columns=["title", "user_id", "deadline", "descript"],
            values=[title, user_id, deadline, descript if descript is not None else "" ]
        )
