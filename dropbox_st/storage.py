from dropbox import Dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import AuthError
from fastapi import UploadFile

from core import Storage


class DropboxStorage(Storage):
    @classmethod
    def upload_file(
        cls,
        file: UploadFile,
        **kwargs,
    ) -> str:
        dbx = cls.get_client(**kwargs)
        upload_result = dbx.files_upload(
            file.file.read(), f"/{file.filename}", mode=WriteMode("overwrite")
        )
        return f"https://www.dropbox.com/preview/{upload_result.name}"

    @classmethod
    def get_client(cls, **kwargs):
        dbx = Dropbox(kwargs["access_token"])
        return dbx
