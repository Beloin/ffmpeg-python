import os.path
from typing import Union
from ffmpeg.ffmpeg_user import FFmpegUser, VSize
from services.file_service import FileService
from services.file_service_interface import DriverException
from services.null_identifiers import NullIdentifiers
from storage.driver import DriverInterface


class VideoService(FileService):
    def __init__(self, driver: DriverInterface, hls_dir: str) -> None:
        super().__init__(driver)
        self._hls_dir = hls_dir
        self._ffmpeg_user = FFmpegUser()
        self._hls_dir = ''
        self._MAIN_FILE_NAME = 'index.m3u8'

    def upload(self, file: Union[str, any], *identifiers: str) -> str:
        r"""
        Upload video transforming it to HLS.

        :param file: Path for the current file.
        :param identifiers: a list of identifiers, passed to Driver
        """
        if type(file) is not str: raise NotImplementedError
        if identifiers is None or len(identifiers) == 0:
            raise NullIdentifiers()

        direct, main_index = self._ffmpeg_user.render_hls_video(
            file, self._hls_dir, [VSize.HD], main_name=self._MAIN_FILE_NAME,
        )

        path, status, info = self._upload_path(direct, *identifiers)

        if status == status.FAIL:
            raise DriverException(info)

        return path

    def _upload_path(self, dir_: str, *identifiers):
        path, status, info = self.driver.upload_file(dir_, *identifiers)

        path = os.path.join(path, self._MAIN_FILE_NAME)

        return path, status, info
