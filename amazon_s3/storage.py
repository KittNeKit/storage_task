import boto3
from fastapi import UploadFile, HTTPException

from core import IStorage


class S3AmazonStorage(IStorage):
    def __init__(self, credentials):
        self.validate_credentials(credentials)
        self.credentials = credentials

    def upload_file(
        self,
        file: UploadFile,
    ) -> str:
        s3_key = file.filename
        bucket_name = self.credentials.get("s3_bucket_name")
        s3_client = self.get_client()

        s3_client.upload_fileobj(
            file.file, bucket_name, s3_key, ExtraArgs={"ContentType": "text/plain"}
        )
        s3_client.put_object_acl(Bucket=bucket_name, Key=s3_key, ACL="public-read")
        return self._get_object_url(bucket_name, s3_key)

    def get_client(self):
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=self.credentials["aws_access_key_id"],
            aws_secret_access_key=self.credentials["aws_secret_access_key"],
        )
        return s3_client

    def get_all_objects(self):
        s3_client = self.get_client()
        bucket_name = self.credentials.get("s3_bucket_name")
        objects = s3_client.list_objects_v2(Bucket=bucket_name)["Contents"]
        objects_url = [
            self._get_object_url(bucket_name, object_instance["Key"])
            for object_instance in objects
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
            raise HTTPException(
                status_code=422, detail="Вкажи ключ доступу амазон, :))))"
            )
        if not credentials.get("aws_secret_access_key"):
            raise HTTPException(status_code=422, detail="Вкажи секретний ключ, :))))")
