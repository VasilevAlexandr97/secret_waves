class S3UploadError(Exception):
    """
    Исключение, выбрасываемое при неудачной загрузке файла в S3.
    Содержит информацию о ключе, бакете и оригинальную ошибку.
    """
    def __init__(self, key: str, bucket: str, original_exception: Exception):
        self.key = key
        self.bucket = bucket
        self.original_exception = original_exception
        message = f"Failed to upload key '{key}' to bucket '{bucket}': {original_exception}"
        super().__init__(message)


class S3DownloadError(Exception):
    def __init__(self, key: str, bucket: str, original_error: Exception):
        self.key = key
        self.bucket = bucket
        self.original_error = original_error
        super().__init__(
            f"Failed to download {key} from {bucket}: {original_error}"
        )

class UnsupportedMimeTypeError(Exception):
    def __init__(self, mime_type: str):
        self.mime_type = mime_type
        message = f"Unsupported mime type: {mime_type}"
        super().__init__(message)