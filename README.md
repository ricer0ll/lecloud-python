# LeCloud Python SDK

Python SDK for LeCloud.  

Installation:  
```bash
pip install lecloud-python
```  

Usage example:  
```python
from lecloud import Credentials, LeCloudClient

credentials = Credentials("example@email.com", "yourpass", "uuidgoeshere")
client = LeCloudClient(credentials, "apikeygoeshere")

try:
    secret = client.get_secret("uuidgoeshere")
    print(secret)
except Exception as e:
    print(e)
```