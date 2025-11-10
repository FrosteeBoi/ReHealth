import hashlib

class User:
    """
    The class represents the user's login details
    """

    def __init__(self, username, password, sex, dob, join_date, user_id=None):
        self.username = username
        self.password = password
        self.sex = sex
        self.dob = dob
        self.join_date = join_date
        self.user_id = user_id

    @staticmethod
    def password_hasher(password):
        """
        Hashes the password securely so it can be stored
        """
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return password_hash

    def password_check(self, input_password):
        """
        Checks if the password inputted through login is the correct one
        """
        return self.password == self.password_hasher(input_password)








