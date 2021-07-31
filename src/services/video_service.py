from typing import Union
from ffmpeg.ffmpeg_user import FFmpegUser, VSize
from services.file_service import FileService
from services.file_service_interface import DriverException
from storage.driver import DriverInterface


class VideoService(FileService):
    _ffmpeg_user = FFmpegUser()
    _stream_dir = 'PUT CONFIG HERE'

    def __init__(self, driver: DriverInterface) -> None:
        super().__init__(driver)

    def upload(self, file: Union[str, any], *identifiers: str) -> str:
        """
        Uploads a video. Converting it into HLS video format.
        """
        if type(file) is not str: raise NotImplementedError

        direct, file = self._ffmpeg_user.render_hls_video(
            file, self._stream_dir, [VSize.FHD, VSize.HD], main_name='index.m3u8',
        )

        self.driver.upload_file(direct, *identifiers)
        path, status, info = self.driver.upload_file(direct)

        if status == status.FAIL:
            raise DriverException(info)

        return path
