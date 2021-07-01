from enum import Enum
from io import BufferedReader
from typing import Literal

from services.file_service import FileService
from services.video_service import VideoService
from storage.drivers.filesystem_driver import FileSystemDriver


class FileType(Enum):
    VIDEO = 'VIDEO'
    FILE = 'FILE'


class DefaultService:
    defaultDriver = FileSystemDriver('./test_files')
    videoService = VideoService(defaultDriver)
    fileService = FileService(defaultDriver)

    def upload_file(self, path: str, file_type: FileType, *identifiers: str) -> str:
        """
        First identifier are the most important.
        The last are used to prevent data replacement.
        """

        if file_type == FileType.VIDEO:
            return self.videoService.upload(path, *identifiers)

        return self.fileService.upload(path, *identifiers)

    def get_file(self, path: str) -> BufferedReader:
        return self.fileService.download(path)

    def delete_file(self, path: str):
        return self.fileService.delete(path)
