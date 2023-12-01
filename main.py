from typing import Any

from fastapi import FastAPI, Request, UploadFile, File, HTTPException, Form
from pydantic import BaseModel

from amazon_s3.storage import S3AmazonStorage
from dropbox_st.storage import DropboxStorage


app = FastAPI()


class StorageFactory:
    def __init__(self, storage_name: str):
        self.storage_name = storage_name

    def factory_method(self, credentials: dict):
        if self.storage_name == "s3_amazon":
            return S3AmazonStorage(credentials)
        elif self.storage_name == "dropbox":
            return DropboxStorage(credentials)


class StorageModel(BaseModel):
    credentials: dict
    name: str


@app.post("/api/upload_file")
async def upload_file(
    request: Request,
    storage_instance: StorageModel,
    text_file: UploadFile = File(),
):
    validate_type_file(text_file)
    storage = StorageFactory(storage_instance.name).factory_method(
        storage_instance.credentials
    )
    text_url = storage.upload_file(text_file)
    return {"text_url": text_url}


@app.get("/api/objects")
async def get_objects(request: Request):
    request_data = await request.json()
    objects = {
        storage_name: StorageFactory(storage_name).factory_method(credentials).get_all_objects()
        for storage_name, credentials in request_data.items()
    }
    return objects


def validate_type_file(file: UploadFile):
    if file.content_type != "text/plain":
        raise HTTPException(status_code=422, detail="Wrong file type, use .txt")
