import os.path
from typing import Union
from ffmpeg.ffmpeg_user import FFmpegUser, VSize
from services.file_service import FileService
from services.file_service_interface import DriverException
from storage.driver import DriverInterface


class VideoService(FileService):
    _ffmpeg_user = FFmpegUser()
    _hls_dir = ''
    _MAIN_FILE_NAME = 'index.m3u8'

    def __init__(self, driver: DriverInterface, hls_dir: str) -> None:
        super().__init__(driver)
        self._hls_dir = hls_dir

    def upload(self, file: Union[str, any], *identifiers: str) -> str:
        """
        Uploads a video. Converting it into HLS video format.
        """
        if type(file) is not str: raise NotImplementedError

        direct, main_index = self._ffmpeg_user.render_hls_video(
            file, self._hls_dir, [VSize.HD], main_name=self._MAIN_FILE_NAME,
        )

        path, status, info = self._upload_dir(direct, *identifiers)

        if status == status.FAIL:
            raise DriverException(info)

        return path

    def _upload_dir(self, dir_: str, *identifiers):
        path, status, info = self.driver.upload_file(dir_, *identifiers)

        path = os.path.join(path, self._MAIN_FILE_NAME)

        return path, status, info
