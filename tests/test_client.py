import unittest
from unittest.mock import MagicMock, patch
import requests

from src.lecloud import LeCloudClient


class TestLeCloudClient(unittest.TestCase):

    def setUp(self):
        self.mock_credentials = MagicMock()
        self.mock_credentials.username = "test_user"
        self.mock_credentials.password = "test_password"
        self.mock_credentials.account_id = "acc_123"

        self.api_key = "mock_api_key"
        self.client = LeCloudClient(self.mock_credentials, self.api_key)

    def test_get_header_without_jwt(self):
        """Should return only the api-key header when no JWT is provided."""
        header = self.client._get_header()
        expected = {"api-key": "mock_api_key"}
        self.assertEqual(header, expected)

    def test_get_header_with_jwt(self):
        """Should include Authorization header when JWT is provided."""
        header = self.client._get_header(jwt="mock_jwt_token")
        expected = {
            "api-key": "mock_api_key",
            "Authorization": "Bearer mock_jwt_token"
        }
        self.assertEqual(header, expected)

    @patch("requests.post")
    def test_get_jwt_success(self, mock_post):
        """Should return the token when the API responds with 200."""
        # Mocking the response object
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"token": "valid_jwt_abc123"}
        mock_post.return_value = mock_response

        token = self.client._get_jwt()

        self.assertEqual(token, "valid_jwt_abc123")
        mock_post.assert_called_once_with(
            url="https://api.riceroll.fyi/v1/jwt",
            headers={"api-key": "mock_api_key"},
            json={"email": "test_user", "password": "test_password"}
        )

    @patch("requests.post")
    def test_get_jwt_failure(self, mock_post):
        """Should raise an Exception if the API status code is not 200."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_post.return_value = mock_response

        with self.assertRaises(Exception) as context:
            self.client._get_jwt()
        
        self.assertIn("Status not 200 for call to get JWT", str(context.exception))

    @patch("requests.get")
    def test_get_secret_success(self, mock_get):
        """Should return the secret value when all API calls succeed."""
        # We need to mock _get_jwt so it doesn't make an actual network call during this test
        with patch.object(self.client, "_get_jwt", return_value="mocked_jwt") as mock_jwt_method:
            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {"secret_value": "super_secret_password"}
            mock_get.return_value = mock_response

            secret = self.client.get_secret("secret_id_999")

            self.assertEqual(secret, "super_secret_password")
            mock_jwt_method.assert_called_once()
            mock_get.assert_called_once_with(
                url="https://api.riceroll.fyi/v1/accounts/acc_123/secrets/secret_id_999/decrypt",
                headers={
                    "api-key": "mock_api_key",
                    "Authorization": "Bearer mocked_jwt"
                }
            )

    @patch("requests.get")
    def test_get_secret_failure(self, mock_get):
        """Should raise an Exception if the get_secret API call returns a non-200 status."""
        with patch.object(self.client, "_get_jwt", return_value="mocked_jwt"):
            mock_response = MagicMock()
            mock_response.status_code = 404
            mock_get.return_value = mock_response

            with self.assertRaises(Exception) as context:
                self.client.get_secret("secret_id_999")

            self.assertIn("Status not 200 for call to get secret", str(context.exception))


if __name__ == "__main__":
    unittest.main()