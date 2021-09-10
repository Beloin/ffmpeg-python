import os.path
import random
import string
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

    def __init__(self):
        pass

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

        output = self._get_output_dir(output)

        video = ff.input(path)
        hls = video.hls(ff.Formats.h264())

        rep = []
        for video_size in video_sizes:
            rep.append(self._get_representation(video_size))

        hls.representations(*rep)

        # New video main file output.
        new_output = join(output, main_name)

        hls.output(new_output)

        return output, new_output

    def _get_output_dir(self, init_dir: str):
        path = self._get_dir(init_dir)
        random_str = self._create_random_str()
        path = join(path, random_str)
        os.makedirs(path)
        return path

    @staticmethod
    def _create_random_str(random_digits=16):
        return ''.join(
            random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=random_digits)
        )

    @staticmethod
    def _get_representation(vide_size: VSize):
        if vide_size == '1080X720':
            return ff.Representation(
                ff.Size(1080, 720), ff.Bitrate(2048 * 2 ^ 10, 320 * 1024))
        elif vide_size == '720X480':
            return ff.Representation(
                ff.Size(720, 480), ff.Bitrate(750 * 1024, 192 * 1024))

        return ff.Representation(ff.Size(1920, 1080), ff.Bitrate(2048 * 1024, 320 * 1024))

    @staticmethod
    def _get_dir(path: str):
        is_abs = os.path.isabs(path)
        if is_abs:
            return path
        return os.path.normpath(os.getcwd() + path)
