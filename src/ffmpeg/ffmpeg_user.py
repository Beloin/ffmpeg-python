import ffmpeg_streaming as ff
from typing import List, Literal, Tuple
from os.path import join

VSize = Literal["1920X1080", "1080X720", "720X480"]


class FFmpegUser:
    """ FFMPEG User. Renders a video. """

    def render_hls_video(self, path: str, output: str, vsizes: List[VSize],
                         main_name='index.m3u8') -> Tuple[str, str]:
        """
        Creates a HLS video from filePath.

        Parameters
        -----------
        path: input path.
        output: file output.
        vsizes: Video sizes.
        main_name: Main HLS video name.

        Returns
        -----------
        output: output, base dir where files where saved.
        video_output: output + /{main_name}.m3u8
        """
        video = ff.input(path)
        hls = video.hls(ff.Formats.h264())

        rep = []
        for vsize in vsizes:
            rep.append(self._get_representation(vsize))

        hls.representations(*rep)

        # New video main file output.
        new_output = join(output, main_name)

        hls.output(new_output)

        return output, new_output

    def _get_representation(self, vsize: VSize):
        if vsize == '1080X720':
            return ff.Representation(
                ff.Size(1080, 720), ff.Bitrate(2048 * 2 ^ 10, 320 * 1024))
        elif vsize == '720X480':
            return ff.Representation(
                ff.Size(720, 480), ff.Bitrate(750 * 1024, 192 * 1024))

        return ff.Representation(ff.Size(1920, 1080), ff.Bitrate(2048 * 1024, 320 * 1024))
