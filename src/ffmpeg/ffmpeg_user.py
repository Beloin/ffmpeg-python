from enum import Enum

import ffmpeg_streaming as ff
from typing import List, Literal, Tuple
from os.path import join


class VSize(Enum):
    """ Video Sizes in an Enum format"""
    FHD = "1920X1080"
    HD = "1080X720"
    HQ = "720X480"


class FFmpegUser:
    """ FFMPEG User. Renders a video. """

    def render_hls_video(self, path: str, output: str, video_sizes: List[VSize],
                         main_name='index.m3u8') -> Tuple[str, str]:
        """
        Creates a HLS video from filePath.

        Parameters
        -----------
        path: input path.
        output: file output.
        video_sizes: Video sizes.
        main_name: Main HLS video name.

        Returns
        -----------
        output: output, base dir where files where saved.
        video_output: output + /{main_name}.m3u8
        """
        video = ff.input(path)
        hls = video.hls(ff.Formats.h264())

        rep = []
        for video_size in video_sizes:
            rep.append(self.__get_representation(video_size))

        hls.representations(*rep)

        # New video main file output.
        new_output = join(output, main_name)

        hls.output(new_output)

        return output, new_output

    @staticmethod
    def __get_representation(vide_size: VSize):
        if vide_size == '1080X720':
            return ff.Representation(
                ff.Size(1080, 720), ff.Bitrate(2048 * 2 ^ 10, 320 * 1024))
        elif vide_size == '720X480':
            return ff.Representation(
                ff.Size(720, 480), ff.Bitrate(750 * 1024, 192 * 1024))

        return ff.Representation(ff.Size(1920, 1080), ff.Bitrate(2048 * 1024, 320 * 1024))
