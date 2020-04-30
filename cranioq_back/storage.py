import os
from storages.backends.azure_storage import AzureStorage


class PublicAzureStorage(AzureStorage):
    account_name = os.environ.get('ACCOUNT_NAME')
    account_key = os.environ.get('ACCOUNT_KEY')
    azure_container = 'cranioq-static'
    expiration_secs = None