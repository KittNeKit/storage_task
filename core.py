from abc import ABC, abstractmethod

from fastapi import UploadFile


class IStorage(ABC):
    @abstractmethod
    def __init__(self, credentials):
        pass

    @abstractmethod
    def upload_file(
        self,
        file: UploadFile,
    ) -> str:
        pass

    @abstractmethod
    def get_client(self):
        pass

    @abstractmethod
    def get_all_objects(self):
        pass

    @staticmethod
    @abstractmethod
    def validate_credentials(credentials: dict):
        pass
