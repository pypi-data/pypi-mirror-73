import pytest
import os
from s3contents import BlobContentsManager
from s3contents.blobmanager import auth_shared_access_signature
from s3contents.ipycompat import TestContentsManager

@pytest.mark.blob
class BlobContentsManagerTestCase(TestContentsManager):
    def setUp(self):
        token = auth_shared_access_signature(
          account_key=os.environ["AZURE_ACCOUNT_KEY"],
          account_name=os.environ["AZURE_ACCOUNT_NAME"]
        )
        self.contents_manager = BlobContentsManager(
            credential=token,
            container_name=os.environ["AZURE_CONTAINER_NAME"],
            account_name=os.environ["AZURE_ACCOUNT_NAME"],
            prefix="notebook"
        )

        self.tearDown()

    def tearDown(self):
        for item in self.contents_manager.fs.ls(""):
            self.contents_manager.fs.rm(item)
        self.contents_manager.fs.init()

    # Overwrites from TestContentsManager

    def make_dir(self, api_path):
        self.contents_manager.new(
            model={"type": "directory"}, path=api_path,
        )
# This needs to be removed or else we'll run the main IPython tests as well.
del TestContentsManager
