import logging

from tempfile import SpooledTemporaryFile
from typing import BinaryIO

import aioboto3

from botocore.exceptions import ClientError

from src.core.files.exceptions import S3DownloadError, S3UploadError
from src.main.config import S3Config

logger = logging.getLogger(__name__)


class S3FileManager:
    def __init__(
        self,
        settings: S3Config,
    ):
        self.bucket_name = settings.bucket_name
        self.client_config = {
            "aws_access_key_id": settings.access_key.get_secret_value(),
            "aws_secret_access_key": settings.secret_key.get_secret_value(),
            "region_name": settings.region_name,
        }
        if settings.endpoint_url is not None:
            self.client_config["endpoint_url"] = settings.endpoint_url

        self.client_config = {
            k: v for k, v in self.client_config.items() if v is not None
        }
        self.session = aioboto3.Session()


    async def upload_fileobj(
        self,
        fileobj: BinaryIO | SpooledTemporaryFile,
        key: str,
        content_type: str | None = None,
    ) -> bool:
        if content_type is None:
            content_type = "application/octet-stream"

        extra_args = {"ContentType": content_type}
        try:
            async with self.session.client("s3", **self.client_config) as s3:
                await s3.upload_fileobj(
                    Fileobj=fileobj,
                    Bucket=self.bucket_name,
                    Key=key,
                    ExtraArgs=extra_args,
                )
                logger.info(f"File {key} uploaded to {self.bucket_name}")
                return True
        except Exception as e:
            logger.exception(f"{e}")
            raise S3UploadError(key, self.bucket_name, e)

    async def generate_presigned_url(
        self,
        key: str,
        expiration: int = 3600,
        method: str = "get_object",
    ) -> str:
        try:
            async with self.session.client("s3", **self.client_config) as s3:
                url =  await s3.generate_presigned_url(
                    ClientMethod=method,
                    Params={
                        "Bucket": self.bucket_name,
                        "Key": key,
                    },
                    ExpiresIn=expiration,
                )
                logger.info(f"Generated presigned URL for {key}, expires in {expiration} seconds")
                return url
        except ClientError as e:
            logger.exception(f"Failed to generate presigned URL for {key}")
            raise S3DownloadError(key, self.bucket_name, e)
        except Exception as e:
            logger.exception(
                f"Unexpected error generating presigned URL for {key}",
            )
            raise S3DownloadError(key, self.bucket_name, e)

    # async def get_file_content(self, key: str) -> bytes | None:
    #     """
    #     Получение содержимого файла из S3 в памяти

    #     Args:
    #         key: Ключ файла в S3

    #     Returns:
    #         Содержимое файла в виде bytes или None при ошибке
    #     """
    #     try:
    #         async with self.session.client('s3', **self.client_config) as s3:
    #             response = await s3.get_object(
    #                 Bucket=self.bucket_name,
    #                 Key=key,
    #             )
    #             content = await response["Body"].read()
    #             self.logger.info(f"Содержимое файла {key} успешно получено")
    #             return content
    #     except Exception:
    #         logger.exception(f"Can't get file content from S3: {key}")
    #         return None