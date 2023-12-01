from abc import ABC, abstractmethod

from fastapi import UploadFile


class Storage(ABC):
    @classmethod
    @abstractmethod
    def upload_file(
        cls,
        file: UploadFile,
        credentials: dict,
    ) -> str:
        pass

    @classmethod
    @abstractmethod
    def get_client(cls, credentials: dict):
        pass

    @classmethod
    @abstractmethod
    def get_all_objects(cls, credentials: dict):
        pass

    @staticmethod
    @abstractmethod
    def validate_credentials(credentials: dict):
        pass
