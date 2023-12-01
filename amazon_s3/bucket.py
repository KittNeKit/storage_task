import boto3
from fastapi import UploadFile, HTTPException

from core import Storage


class AmazonBucket(Storage):
    @classmethod
    def upload_file(
        cls,
        file: UploadFile,
        credentials: dict,
    ) -> str:
        s3_key = file.filename
        bucket_name = credentials.pop("s3_bucket_name")
        s3_client = cls.get_client(credentials)

        s3_client.upload_fileobj(
            file.file, bucket_name, s3_key, ExtraArgs={"ContentType": "text/plain"}
        )
        s3_client.put_object_acl(Bucket=bucket_name, Key=s3_key, ACL="public-read")
        return cls._get_object_url(bucket_name, s3_key)

    @classmethod
    def get_client(cls, credentials: dict):
        cls.validate_credentials(credentials)
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=credentials["aws_access_key_id"],
            aws_secret_access_key=credentials["aws_secret_access_key"],
        )
        return s3_client

    @classmethod
    def get_all_objects(cls, credentials: dict):
        s3_client = cls.get_client(credentials)
        bucket_name = credentials.get("s3_bucket_name")
        objects = s3_client.list_objects_v2(Bucket=bucket_name)["Contents"]
        objects_url = [
            cls._get_object_url(bucket_name, object["Key"]) for object in objects
        ]
        return objects_url

    @staticmethod
    def _get_object_url(bucket_name, s3_key):
        return f"https://{bucket_name}.s3.eu-central-1.amazonaws.com/{s3_key}"

    @staticmethod
    def validate_credentials(credentials: dict):
        if not credentials.get("s3_bucket_name"):
            raise HTTPException(status_code=422, detail="Вкажи нейм бакету, :))))")
        if not credentials.get("aws_access_key_id"):
            raise HTTPException(status_code=422, detail="Вкажи ключ доступу, :))))")
        if not credentials.get("aws_secret_access_key"):
            raise HTTPException(status_code=422, detail="Вкажи секретний ключ, :))))")
