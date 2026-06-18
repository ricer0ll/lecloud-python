import requests
from .credentials import Credentials

class LeCloudClient:
    def __init__(self, credentials: Credentials, api_key: str):
        self.credentials = credentials
        self.api_key = api_key

    def _get_header(self, jwt=""):
        header = {
            "api-key": self.api_key
        }
        
        if jwt:
            header["Authorization"] = "Bearer " + jwt
        
        return header


    def _get_jwt(self) -> str:
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
        account_id: str = self.credentials.account_id

        response = requests.get(
            url=f"https://api.riceroll.fyi/v1/accounts/{account_id}/secrets/{secret_id}/decrypt",
            headers=self._get_header(self._get_jwt())
        )

        if response.status_code != 200:
            raise Exception("Status not 200 for call to get secret")
        
        secret_value: str = response.json()["secret_value"]
        return secret_value

