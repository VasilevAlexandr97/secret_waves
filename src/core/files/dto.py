from dataclasses import dataclass
from typing import BinaryIO


@dataclass
class FileDTO:
    mime_type: str
    file: BinaryIO
    file_id: str | None = None