"""
Contain most of user methods
"""

from infrastructure.data.password_hasher import PasswordHasher


class UserAuthentication:
    """
    Class used to control user connexion and disconnection
    """

    def __init__(self, db_controller):
        self.db_controller = db_controller
        self.hasher = PasswordHasher()

    def login(self, email, password):
        """
        :param email: user email enter on logon
        :param password: user password enter on logon
        :return: token if user credentials is ok, False if is not
        """
        result = self.db_controller.select(
            table="USERS",
            select="username",
            columns=["email", "passwd"],
            values=[email, self.hasher.hash_password(password)]
        )

        if not result:
            return False

        if result is None:
            return False

        return True


    def get_user_id(self, email):
        """
        Get user id
        :param email: user email
        :param token: user token
        :return: user id if user exist, False if not  
        """
        user_id = self.db_controller.select(
            table="USERS",
            select="id",
            columns="email",
            values=email
        )
        if user_id is not None:
            return user_id
        return False
