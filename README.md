# LeCloud Python SDK

Python SDK for LeCloud.  

Usage example:  
```python
from lecloud import Credentials, LeCloudClient

credentials = Credentials("example@email.com", "yourpass", "uuidgoeshere")
client = LeCloudClient(credentials, "apikeygoeshere")

try:
    secret = client.get_secret("uuidgoeshere")
except Exception as e:
    print(e)

print(secret)
```