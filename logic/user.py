import hashlib


class User:
    """
    User class created, containing user information and methods for handling register/login
    """

    def __init__(self, username, password, sex, dob, join_date, user_id=None):
        self.username = username
        self.password = password
        self.sex = sex
        self.dob = dob
        self.join_date = join_date
        self.user_id = user_id

    @staticmethod
    def password_hasher(password: str) -> str:
        """
        Hashes the password securely so it can be stored

        Args: password: The user's password.

        Returns: a hash created from the password
        """
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return password_hash

    def password_check(self, input_password: str) -> bool:
        """
        Checks password input

        Args: input_password: The password inputted by the user

        Returns: Whether or not the password is correct.
        """
        return self.password == self.password_hasher(input_password)
