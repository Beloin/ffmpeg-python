from typing import List
from services.file_service import FileService
from services.video_service import VideoService


class DefaultService:
    defaulDriver = None
    videoService = VideoService(defaulDriver)
    fileService = FileService(defaulDriver)

    def upload_file(self, path: str, *identifiers: str) -> str:
        """
        First identifier are the most important.
        But the last ones are used to prevent data replace.
        """

        return 'Lol my man'

    def get_file(self, path: str):
        return 'Lol my man'

    def delete_file(self, path: str):
        return 'Lol my man'
