import json
from urllib.parse import urlparse

from traitlets import Any

from s3contents.genericmanager import GenericContentsManager, from_dict
from s3contents.ipycompat import Unicode
from s3contents.blob_fs import BlobFS
import logging
logger = logging.getLogger()
logger.setLevel('DEBUG')

class BlobContentsManager(GenericContentsManager):
    account_name = Unicode(
        help="Azure account name", allow_none=False
    ).tag(config=True, env="JPYNB_AZURE_ACCOUNT_NAME")
    
    container_name = Unicode("notebooks", help="Container name to store notebooks").tag(
        config=True, env="JPYNB_AZURE_CONTAINER_NAME"
    )

    credential = Unicode(help="Azure blob storage").tag(config=True, env="JPYNB_AZURE_CREDENTIAL")

    prefix = Unicode("", help="Prefix path inside the specified bucket").tag(
        config=True
    )

    delimiter = Unicode("/", help="Path delimiter").tag(config=True)
    init_blob_hook = Any(help="optional hook for init blob").tag(config=True)

    def __init__(self, *args, **kwargs):
        super(BlobContentsManager, self).__init__(*args, **kwargs)
        self.run_init_blob_hook()
        self.new_fs()


    def run_init_blob_hook(self):
        if self.init_blob_hook is not None:
            self.init_blob_hook(self)
    
    def new_fs(self):
        self._fs = BlobFS(
            log=self.log,
            credential=self.credential,
            container_name=self.container_name,
            account_name=self.account_name,
            prefix=self.prefix,
            delimiter=self.delimiter
        )

# https://github.com/Azure/azure-sdk-for-python/blob/master/sdk/storage/azure-storage-blob/samples/blob_samples_authentication.py#L110
def auth_shared_access_signature(account_name, account_key, expiry=None):
    # [START create_sas_token]
    # Create a SAS token to use to authenticate a new client
    from datetime import datetime, timedelta
    from azure.storage.blob import ResourceTypes, AccountSasPermissions, generate_account_sas
    
    expiry = expiry if expiry is not None else datetime.utcnow() + timedelta(hours=1)
    sas_token = generate_account_sas(
        account_name,
        account_key=account_key,
        resource_types=ResourceTypes(service=False, container=True, object=True),
        permission=AccountSasPermissions(read=True, write=True, delete=True, list=True, add=True, create=True, update=True, process=True),
        expiry=expiry
    )
    
    return sas_token