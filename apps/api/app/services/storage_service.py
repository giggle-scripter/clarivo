from dataclasses import dataclass
from typing import Any, BinaryIO

import boto3
from botocore.client import BaseClient
from botocore.config import Config
from botocore.exceptions import ClientError

from app.core.config import Settings


@dataclass(frozen=True)
class StoredAudio:
    body: Any
    content_length: int
    content_type: str


class StorageService:
    def __init__(self, settings: Settings) -> None:
        self.bucket = settings.s3_bucket
        self.client: BaseClient = boto3.client(
            "s3",
            endpoint_url=settings.s3_endpoint,
            aws_access_key_id=settings.s3_access_key,
            aws_secret_access_key=settings.s3_secret_key,
            region_name=settings.s3_region,
            config=Config(
                signature_version="s3v4",
                s3={"addressing_style": "path"},
            ),
        )

    def ensure_bucket(self) -> None:
        try:
            self.client.head_bucket(Bucket=self.bucket)
        except ClientError as error:
            error_code = str(error.response.get("Error", {}).get("Code", ""))
            if error_code not in {"404", "NoSuchBucket", "NotFound"}:
                raise
            self.client.create_bucket(Bucket=self.bucket)

    def put_audio(
        self,
        *,
        object_key: str,
        file: BinaryIO,
        content_type: str,
    ) -> str:
        self.ensure_bucket()
        file.seek(0)
        self.client.upload_fileobj(
            file,
            self.bucket,
            object_key,
            ExtraArgs={"ContentType": content_type},
        )
        return f"s3://{self.bucket}/{object_key}"

    def get_audio(self, object_uri: str) -> StoredAudio:
        prefix = f"s3://{self.bucket}/"
        if not object_uri.startswith(prefix):
            raise ValueError("Audio URI does not belong to the configured bucket")
        object_key = object_uri.removeprefix(prefix)
        response = self.client.get_object(Bucket=self.bucket, Key=object_key)
        return StoredAudio(
            body=response["Body"],
            content_length=int(response["ContentLength"]),
            content_type=str(response.get("ContentType") or "application/octet-stream"),
        )
