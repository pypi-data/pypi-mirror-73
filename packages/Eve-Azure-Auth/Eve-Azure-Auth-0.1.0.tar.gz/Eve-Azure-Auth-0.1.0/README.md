# Eve Azure AD Auth

> Under development, it only validate token. Pull requests are welcome

## Read more

https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-protocols-oidc

## Usage

```bash
pip install Eve-Azure-Auth
```

## Setting up configuration

```python
AZURE_AD_TENANT = 'common'  # optional
AZURE_AD_ISSUER = 'https://login.microsoftonline.com/...'
AZURE_AD_AUDIENCES = 'id' # or ['id', 'id']
```

## Initialization

```python
from eve_azure_ad_auth import AzureAuth

app = Eve(auth=AzureAuth)
```

*Voilà!*
