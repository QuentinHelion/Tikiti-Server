"""
CreateUser permit to add user on inscription for him
or creation by admin
"""

import re
from infrastructure.data.password_hasher import PasswordHasher

class CreateUser:
    """
    Class used to create user and save it on db
    """

    def __init__(self, controller):
        self.controller = controller
        self.hasher = PasswordHasher()
        self.table_name = "USERS"

    def create(self, username, email, password):
        """
        :param email: user email
        :param password:  user password
        :return: query result (if working: id of user)
        """
        if not self.is_valid_email(email):
            return False

        try:
            pass_hash = self.hasher.hash_password(password)
        except ValueError as error:
            print(error)
            return False

        result = self.controller.insert(
            table="USERS",
            columns=["username", "email", "passwd"],
            values=[username, email, pass_hash]
        )

        return result

    @staticmethod
    def is_valid_email(email):
        """
        Checks if an email address is valid.
        :param email: str, email to validate
        :return: bool, True if email is valid, else False
        """
        email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        if not re.match(email_regex, email):
            return False
        return True