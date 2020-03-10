from storages.backends.azure_storage import AzureStorage


class PublicAzureStorage(AzureStorage):
    account_name = 'cranioqstatic'
    account_key = '2oSgUNatzP6/RjM+YbowYM3SjCvZUIrxBBB7E1t4q4VW/v5yng3WeP+AlYYrS85nPVn765jV1mWjc4yovg/oew=='
    azure_container = 'cranioq-static'
    expiration_secs = None