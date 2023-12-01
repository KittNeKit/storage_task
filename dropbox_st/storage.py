from dropbox import Dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import AuthError
from fastapi import UploadFile, HTTPException

from core import Storage


class DropboxStorage(Storage):
    @classmethod
    def upload_file(
        cls,
        file: UploadFile,
        credentials: dict,
    ) -> str:
        dbx = cls.get_client(credentials)
        upload_result = dbx.files_upload(
            file.file.read(), f"/{file.filename}", mode=WriteMode("overwrite")
        )
        return f"https://www.dropbox.com/preview/{upload_result.name}"

    @classmethod
    def get_client(cls, credentials: dict):
        cls.validate_credentials(credentials)
        dbx = Dropbox(credentials.get("access_token"))
        return dbx

    @classmethod
    def get_all_objects(cls, credentials: dict):
        dbx = cls.get_client(credentials)
        objects = dbx.files_list_folder(path="")
        objects_url = [cls._get_object_url(object.name) for object in objects.entries]
        return objects_url

    @staticmethod
    def _get_object_url(key):
        return f"https://www.dropbox.com/preview/{key}"

    @staticmethod
    def validate_credentials(credentials: dict):
        if not credentials.get("access_token"):
            raise HTTPException(status_code=422, detail="Вкажи ключ доступу, :))))")
