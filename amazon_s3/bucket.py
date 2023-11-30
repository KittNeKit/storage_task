import boto3
from fastapi import UploadFile

from core import Storage


class AmazonBucket(Storage):
    @classmethod
    def upload_file(
        cls,
        file: UploadFile,
        **kwargs,
    ) -> str:
        s3_key = file.filename
        bucket_name = kwargs.pop("s3_bucket_name")
        s3_client = cls.get_client(**kwargs)

        s3_client.upload_fileobj(
            file.file, bucket_name, s3_key, ExtraArgs={"ContentType": "text/plain"}
        )
        s3_client.put_object_acl(Bucket=bucket_name, Key=s3_key, ACL="public-read")
        return f"https://{bucket_name}.s3.eu-central-1.amazonaws.com/{s3_key}"

    @classmethod
    def get_client(cls, **kwargs):
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=kwargs["aws_access_key_id"],
            aws_secret_access_key=kwargs["aws_secret_access_key"],
        )
        return s3_client
