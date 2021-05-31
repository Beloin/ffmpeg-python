from typing import Union
from ffmpeg.ffmpeg_user import FFmpegUser
from services.file_service import FileService
from storage.driver import DriverInterface
from .file_service_interface import (DriverException)


class VideoService(FileService):
    _ffmpeg_user = FFmpegUser()
    _stream_dir = 'PUT CONFIG HERE'

    def __init__(self, driver: DriverInterface) -> None:
        super().__init__(driver)

    def upload(self, file: Union[str, any], *identifiers: str) -> str:
        """
        Uploads a video. Converting it into HLS video format.
        """
        if type(file) is str:
            dir, file = self._ffmpeg_user.render_hls_video(
                file, self._stream_dir, ["1080X720", "720X480"], main_name='index.m3u8',
            )
            self.driver.upload_file(dir, *identifiers)

        else:
            raise NotImplementedError

        self.driver.upload_file(dir)
