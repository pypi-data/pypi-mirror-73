"""
Utilities to make S3 look like a regular file system
"""
import base64
import os
import sys

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azure.core.exceptions import ResourceNotFoundError
from botocore.exceptions import ClientError
from tornado.web import HTTPError
from traitlets import Any

from s3contents.genericfs import GenericFS, NoSuchFile
from s3contents.ipycompat import Unicode


class BlobFS(GenericFS):

    credential = Unicode(
        help="Azure Credential", allow_none=False
    ).tag(config=True, env="JPYNB_AZURE_CREDENTIAL")
    
    account_name = Unicode(
        help="Azure account name", allow_none=False
    ).tag(config=True, env="JPYNB_AZURE_ACCOUNT_NAME")

    container_name = Unicode(help="Container name to store notebooks").tag(
        config=True, env="JPYNB_AZURE_CONTAINER_NAME"
    )
    prefix = Unicode("", help="Prefix path inside the specified bucket").tag(
        config=True
    )
    delimiter = Unicode("/", help="Path delimiter").tag(config=True)

    dir_keep_file = Unicode(
        ".blobkeep", help="Empty file to create when creating directories"
    ).tag(config=True)

    def __init__(self, log, **kwargs):
        super(BlobFS, self).__init__(**kwargs)
        self.log = log
        self.account_url = f"https://{self.account_name}.blob.core.windows.net"
        self.container_client = ContainerClient(
            account_url=self.account_url,
            container_name=self.container_name,
            credential=self.credential
        )
        self.init()

    def init(self):
        try:
            self.mkdir("")
            self.ls("")
            self.isdir("")
        except ClientError as ex:
            if "AccessDenied" in str(ex):
                
                self.log.error("AccessDenied error")
                sys.exit(1)
            else:
                raise ex

    #  GenericFS methods -----------------------------------------------------------------------------------------------

    def ls(self, path=""):
        path_ = self.path(path)
        self.log.debug("Blobcontents.BlobFS.ls: Listing directory: `%s`", path_)
        blob_list = self.container_client.list_blobs(name_starts_with=path_)
        files = list(map(lambda blob: blob.name, blob_list))
        self.log.debug("Blobcontents.BlobFS.ls: files: `%s`", files)
        files = list(map(lambda name: self.blob_mapper(name, path_), files))
        self.log.debug("Blobcontents.BlobFS.ls: mapped files: `%s`", files)
        # unique
        files = list(set(files))
        self.log.debug("Blobcontents.BlobFS.ls: unique files: `%s`", files)
        return self.unprefix(files)

    def isfile(self, path):
        path_ = self.path(path)
        is_file = True
        self.log.debug("Blobcontents.BlobFS.isfile: path: %s", path)
        try:
            blob_client = self.container_client.get_blob_client(path_)
            blob_client.get_blob_properties()
        except (ResourceNotFoundError, ValueError) as e:
            is_file = False
        self.log.debug("Blobcontents.BlobFS: `%s` is a blob: %s", path, is_file)
        return is_file
    
    def isdir(self, path):
        path_ = self.path(path, self.dir_keep_file)
        blob_client = self.container_client.get_blob_client(path_)
        is_dir = True
        try:
            blob_client.get_blob_properties()
        except ResourceNotFoundError:
            is_dir = False
        self.log.debug("Blobcontents.BlobFS: `%s` is a directory: %s", path, is_dir)
        return is_dir

    def mv(self, old_path, new_path):
        self.log.debug("Blobcontents.BlobFS: Move from `%s` to `%s`", old_path, new_path)
        self.cp(old_path, new_path)
        self.rm(old_path)

    def cp(self, old_path, new_path):
        old_path_, new_path_ = self.path(old_path), self.path(new_path)
        self.log.debug("Blobcontents.BlobFS: Coping `%s` to `%s`", old_path_, new_path_)

        if self.isdir(old_path):
            old_dir_path, new_dir_path = old_path, new_path
            for obj in self.ls(old_dir_path):
                old_item_path = obj
                new_item_path = old_item_path.replace(old_dir_path, new_dir_path, 1)
                self.log.debug("Blobcontents.BlobFS.cp: old item path `%s`, new item path`%s`", old_item_path, new_item_path)
                self.cp(old_item_path, new_item_path)
            self.mkdir(new_dir_path)  # Touch with dir_keep_file
        elif self.isfile(old_path):
            old_blob_url = f"{self.account_url}/{self.container_name}/{old_path_}?{self.credential}"
            self.log.debug("Blobcontents.BlobFS: old blob url `%s` to new `%s`", old_blob_url, new_path_)
            new_blob = self.container_client.get_blob_client(new_path_)
            new_blob.start_copy_from_url(old_blob_url)
            status = 'pending'
            while status == 'pending':
                properties = new_blob.get_blob_properties()
                status = properties.copy.status

    def rm(self, path):
        path_ = self.path(path)
        self.log.debug("Blobcontents.BlobFS: Removing: `%s`", path_)
        if self.isfile(path):
            self.log.debug("Blobcontents.BlobFS: Removing file: `%s`", path_)
            self.container_client.delete_blob(path_, delete_snapshots="include")
        elif self.isdir(path):
            self.log.debug("Blobcontents.BlobFS: Removing directory: `%s`", path_)
            blob_list = self.container_client.list_blobs(name_starts_with=path_ + '/')
            files = list(map(lambda blob: blob.name, blob_list))
            self.log.debug("Blobcontents.BlobFS: Removing blobs: `%s`", files)
            for file in files:
                self.container_client.delete_blob(self.path(file), delete_snapshots="include")

    def mkdir(self, path):
        path_ = self.path(path, self.dir_keep_file)
        self.log.debug("Blobcontents.BlobFS: Making dir: `%s`", path)
        blob_client = self.container_client.upload_blob(path_, data=b"", overwrite=True)
        properties = blob_client.get_blob_properties()
        self.log.debug("Blobcontents.BlobFS: Made dir: `%s`", properties)


    def read(self, path, format):
        path_ = self.path(path)
        self.log.debug("Blobcontents.BlobFS.read: Reading file: `%s`", path_)
        if not self.isfile(path):
            raise NoSuchFile(path_)
        downloader = self.container_client.download_blob(path_)
        if format is None or format == "text":
            return downloader.content_as_text(), "text"
        return base64.b64encode(downloader.content_as_bytes()).decode("ascii"), "base64"

    def lstat(self, path):
        path_ = self.path(path)
        if self.isdir(path_):  # Try to get status of the dir_keep_file
            path_ = self.path(path, self.dir_keep_file)
        try:
            blob_client = self.container_client.get_blob_client(path_)
            properties = blob_client.get_blob_properties()
        except:
            return {"ST_MTIME": None} 
        ret = {}
        ret["ST_MTIME"] = properties.last_modified
        return ret

    def write(self, path, content, format="text"):
        path_ = self.path(self.unprefix(path))
        self.log.debug("Blobcontents.BlobFS: Writing file: `%s`", path_)
        if format not in {"text", "base64"}:
            raise HTTPError(
                400, "Must specify format of file contents as 'text' or 'base64'",
            )
        try:
            if format == "text":
                content_ = content.encode("utf8")
            else:
                b64_bytes = content.encode("ascii")
                content_ = base64.b64decode(b64_bytes)
        except Exception as e:
            raise HTTPError(400, "Encoding error saving %s: %s" % (path_, e))
        self.container_client.upload_blob(path_, data=content_,  overwrite=True)

    def writenotebook(self, path, content):
        path_ = self.path(self.unprefix(path))
        self.log.debug("Blobcontents.BlobFS: Writing notebook: `%s`", path_)
        self.container_client.upload_blob(path_, data=content.encode("utf-8"),  overwrite=True)
    #  Utilities -------------------------------------------------------------------------------------------------------

    def unprefix(self, path):
        """Remove the self.prefix_ (if present) from a path or list of paths"""
        self.log.debug(f"BlobFS.unprefix: self.prefix: {self.prefix} path: {path}")
        if isinstance(path, str):
            path = path[len(self.prefix) :] if path.startswith(self.prefix) else path
            path = path[1:] if path.startswith(self.delimiter) else path
            return path
        if isinstance(path, (list, tuple)):
            path = [
                p[len(self.prefix) :] if p.startswith(self.prefix) else p
                for p in path
            ]
            path = [p[1:] if p.startswith(self.delimiter) else p for p in path]
            return path

    def path(self, *path):
        """Utility to join paths including the bucket and prefix"""
        path = list(filter(None, path))
        path = self.unprefix(path)
        items = [self.prefix] + path if self.prefix != '' else path
        self.log.debug("Blobcontents.BlobFS.path: origin: `%s`, new: `%s`", path, items)
        return self.delimiter.join(items)

    def blob_mapper(self, name, name_starts_with):
        if (name_starts_with == ""):
            return name.split(self.delimiter)[0]
        else:
            count = name_starts_with.count(self.delimiter) + 2
            return self.delimiter.join(name.split(self.delimiter)[0:count])