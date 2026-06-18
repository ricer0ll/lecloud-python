class Credentials:
    """A data class that stores authentication credentials and account metadata.

    Attributes:
        username (str): The email or username associated with the account.
        password (str): The password used for authentication.
        account_id (str): The unique identifier for the cloud provider account.
    """

    def __init__(self, username: str, password: str, account_id: str):
        """Initializes the Credentials instance with user and account details."""
        self.username = username
        self.password = password
        self.account_id = account_id