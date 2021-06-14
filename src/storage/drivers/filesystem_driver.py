from io import BufferedReader
import os
from os.path import join, normpath, isfile
import shutil

from typing import Tuple, Union
from storage.driver import DriverInterface, Status


class FileSystemDriver(DriverInterface):
    """ Driver thats saves files in computes's current filesystem."""

    def __init__(self, save_dir) -> None:
        super().__init__()

        self.save_dir = save_dir

    def upload_file(self, file: Union[str, any], *identifiers: str, file_name: str = None) -> Tuple[str, Status, str]:
        to_save = self._normajoin(self.save_dir, *identifiers)
        print(to_save)

        if type(file) is str:
            try:
                to_path = self._create_dir(*identifiers, file_name=file_name)
                shutil.move(file, to_path)
                return to_path, 'OK', 'File saved successfully'
            except Exception as e:
                return None, 'FAIL', str(e)

        # If is not file. We don't have yet an implementation.
        raise Exception('File not sent in str like.')

    def delete_file(self, path: str) -> Tuple[Status, str]:
        try:
            path = self._normajoin(self.save_dir, path)
            os.remove(path)

            return 'OK', 'File deleted successfully'
        except Exception as e:
            return 'FAIL', str(e)

    def download_file(self, path: str) -> Tuple[any, Status, str]:
        try:
            reader = self._read_file(path)
            return reader, 'OK', 'File sent in Buffer.'
        except Exception as e:
            return None, 'FAIL', str(e)

    # Private Methods
    def _read_file(self, path: str) -> BufferedReader:
        if not isfile(path):
            raise Exception('Path needs to be a file.')
        f = open(path, 'rb')

        return f

    def _normajoin(*paths: str):
        return normpath(join(*paths))

    def _create_dir(self, *identifiers: str, file_name: str = None) -> str:
        """
        If `file_name` is None, last id is used as file_name.

        Returns
        --------
        path to file. (obs: File is not created.)
        """

        if file_name:
            path = self._normajoin(*identifiers)
            return self._normajoin(path, file_name)

        file = identifiers[len(identifiers)-1]
        dirs = identifiers[:len(identifiers)-1]

        path = self._normajoin(self.save_dir, *dirs)
        os.makedirs(path)

        return self._normajoin(path, *file)
