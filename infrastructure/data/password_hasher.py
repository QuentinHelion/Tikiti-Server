"""
Module to manage password hashing
"""

import hashlib

class PasswordHasher:
    """
    Class used to hash user passwords
    """

    def __init__(self, algorithm="sha256"):
        self.algorithm = algorithm

    def hash_password(self, password):
        """
        Hashes a password using the specified algorithm.

        :param password: str, the password to hash
        :return: str, the hashed password
        """
        salt = hashlib.sha256(password.encode()).hexdigest().encode()
        hashed_password = hashlib.pbkdf2_hmac(self.algorithm, password.encode(), salt, 100000)
        return hashed_password.hex()

    def verify_password(self, password, hashed_password):
        """
        Verifies a password against a hashed password.

        :param password: str, the password to verify
        :param hashed_password: str, the hashed password to compare against
        :return: bool, True if the passwords match, else False
        """
        return hashed_password == self.hash_password(password)