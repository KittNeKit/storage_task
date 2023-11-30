from abc import ABC, abstractmethod

from fastapi import UploadFile


class Storage(ABC):
    @classmethod
    @abstractmethod
    def upload_file(
        cls,
        file: UploadFile,
        **kwargs,
    ) -> str:
        pass

    @classmethod
    @abstractmethod
    def get_client(cls, **kwargs):
        pass
