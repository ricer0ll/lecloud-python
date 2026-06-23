import requests
from .credentials import Credentials

class LeCloudClient:
    """A client for interacting with the LeCloud API to manage and retrieve secrets.

    Attributes:
        credentials (Credentials): An instance containing authentication details.
        api_key (str): The API key used for basic request authentication.
    """

    def __init__(self, credentials: Credentials, api_key: str):
        """Initializes the LeCloudClient with credentials and an API key."""
        self.credentials = credentials
        self.api_key = api_key

        self.jwt = self._get_jwt()

    def _get_header(self, jwt="") -> dict:
        """Constructs the HTTP headers required for API requests.

        Args:
            jwt (str, optional): A JSON Web Token for Bearer authentication. 
                Defaults to an empty string.

        Returns:
            dict: A dictionary containing the constructed headers.
        """
        header = {
            "api-key": self.api_key
        }
        
        if jwt:
            header["Authorization"] = "Bearer " + jwt
        
        return header


    def _get_jwt(self) -> str:
        """Authenticates with the server using credentials to retrieve a JWT.

        Returns:
            str: The JWT token string.

        Raises:
            Exception: If the server returns a non-200 status code.
        """
        payload = {
            "email": self.credentials.username,
            "password": self.credentials.password
        }

        response = requests.post(
            url="https://api.riceroll.fyi/v1/jwt",
            headers=self._get_header(),
            json=payload
        )

        if response.status_code != 200:
            raise Exception("Status not 200 for call to get JWT")
        
        token: str = response.json()["token"]
        return token


    def get_secret(self, secret_id: str) -> str:
        """Retrieves and decrypts a specific secret from the cloud provider.

        Args:
            secret_id (str): The unique identifier of the secret to fetch.

        Returns:
            str: The decrypted secret value.

        Raises:
            Exception: If the server returns a non-200 status code.
        """
        account_id: str = self.credentials.account_id

        response = requests.get(
            url=f"https://api.riceroll.fyi/v1/accounts/{account_id}/secrets/{secret_id}/decrypt",
            headers=self._get_header(self.jwt)
        )

        if response.status_code != 200:
            raise Exception("Status not 200 for call to get secret")
        
        secret_value: str = response.json()["secret_value"]
        return secret_value