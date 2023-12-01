from dropbox import Dropbox
from dropbox.files import WriteMode
from fastapi import UploadFile, HTTPException

from core import IStorage


class DropboxStorage(IStorage):
    def __init__(self, credentials):
        self.validate_credentials(credentials)
        self.credentials = credentials

    def upload_file(
        self,
        file: UploadFile,
    ) -> str:
        dbx = self.get_client()
        upload_result = dbx.files_upload(
            file.file.read(), f"/{file.filename}", mode=WriteMode("overwrite")
        )
        return f"https://www.dropbox.com/preview/{upload_result.name}"

    def get_client(self):
        dbx = Dropbox(self.credentials.get("access_token"))
        return dbx

    def get_all_objects(self):
        dbx = self.get_client()
        objects = dbx.files_list_folder(path="")
        objects_url = [
            self._get_object_url(object_instance.name)
            for object_instance in objects.entries
        ]
        return objects_url

    @staticmethod
    def _get_object_url(key):
        return f"https://www.dropbox.com/preview/{key}"

    @staticmethod
    def validate_credentials(credentials: dict):
        if not credentials.get("access_token"):
            raise HTTPException(status_code=422, detail="Вкажи ключ доступу, :))))")
