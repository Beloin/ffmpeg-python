from io import BufferedReader
from services.file_service import FileService
from services.video_service import VideoService
from storage.drivers.filesystem_driver import FileSystemDriver


class DefaultService:
    defaulDriver = FileSystemDriver('./test_files')
    videoService = VideoService(defaulDriver)
    fileService = FileService(defaulDriver)

    def upload_file(self, path: str, *identifiers: str) -> str:
        """
        First identifier are the most important.
        But the last ones are used to prevent data replace.
        """

        return 'Lol my man'

    def get_file(self, path: str) -> BufferedReader:
        return self.fileService.download(path)

    def delete_file(self, path: str):
        return self.fileService.delete(path)
