"""
Contain all method to user (de)connexion
"""

from infrastructure.data.password_hasher import PasswordHasher


class UserAuthentication:
    """
    Class used to control user connexion and disconnection
    """

    def __init__(self, db_controller):
        self.controller = db_controller
        self.hasher = PasswordHasher()

    def login(self, email, password):
        """
        :param email: user email enter on logon
        :param password: user password enter on logon
        :return: token if user credentials is ok, False if is not
        """
        result = self.controller.select(
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

    # def logout(self, email, token):
    #     """
    #     Invalidate the user session associated with the given token
    #     """
    #     user = self.user_presenter.get_user_token(email, token)
    #     print(user)
    #     if user is not None:
    #         result = self.uc_update_user.remove_token(
    #             user_id=user
    #         )
    #         return result
    #     return False

    # def get_user_id(self, email, token):
    #     """
    #     Get user id
    #     :param email: user email
    #     :param token: user token
    #     """
    #     user_id = self.user_presenter.get_user_token(email, token)
    #     if user_id is not None:
    #         return user_id
    #     return False
