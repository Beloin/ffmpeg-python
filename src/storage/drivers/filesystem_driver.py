import re
import string
from functools import reduce
from io import BufferedReader
import os
from os.path import join, normpath, isfile
import shutil
import random
from typing import Tuple, Union, BinaryIO
from storage.driver import DriverInterface, Status


class FileSystemDriver(DriverInterface):
    """ Driver that saves files in computer's current filesystem."""

    def __init__(self, save_dir: str) -> None:
        """
        Parameters:
            save_dir: str represents where to save the files.
        """
        super().__init__()

        self.save_dir = save_dir

    def upload_file(self, file_: Union[str, any], *identifiers: str, file_name: str = None) -> Tuple[
        Union[str, None], Status, str
    ]:
        if type(file_) is str:
            try:
                return self._save(file_, identifiers)
            except Exception as e:
                return None, Status.FAIL, str(e)

        # If is not file. We don't have yet an implementation.
        raise Exception('File not sent in str like.')

    def delete_file(self, path: str) -> Tuple[Status, str]:
        try:
            path = join(self.__get_save_path(), path)
            os.remove(path)

            return Status.OK, 'File deleted successfully'
        except Exception as e:
            return Status.FAIL, str(e)

    def download_file(self, path: str) -> Tuple[Union[BinaryIO, None], Status, str]:
        try:
            reader = self.__read_file(path)
            return reader, Status.OK, 'File sent in Buffer.'
        except Exception as e:
            return None, Status.FAIL, str(e)

    # Private Methods
    def __read_file(self, relative_path: str) -> BinaryIO:
        save_path = self.__get_save_path()
        full_path = join(save_path, relative_path)

        if not isfile(full_path):
            raise Exception('Path needs to be a file.')
        f = open(full_path, 'rb')

        return f

    @staticmethod
    def __normajoin(*paths: str):
        return normpath(join(*paths))

    @staticmethod
    def __join_cwd(*paths: str):
        cwd = os.getcwd()
        path = join(*paths)
        return cwd + path

    def __get_save_path(self):
        """
        Get the save_dir full path.
        """
        return normpath(self.__join_cwd(self.save_dir))

    def _save(self, file_path, *identifiers):
        if os.path.isdir(file_path):
            return self._save_dir(file_path, *identifiers)
        return self._save_file(file_path, *identifiers)

    def _save_file(self, file_path, *identifiers):
        random_id, full_path = self.__create_directory()
        file_name = self.__create_file_name(*identifiers)
        arq_type = self.__get_arq_type(file_path)

        file_name = file_name + arq_type
        full_path = join(full_path, file_name)

        shutil.move(file_path, full_path)

        relative_id = join(random_id, file_name)

        return relative_id, Status.OK, 'File saved successfully'

    def _save_dir(self, file_path, *identifiers):
        random_id, full_path = self.__create_directory()
        file_name = self.__create_file_name(*identifiers)

        full_path = join(full_path, file_name)

        shutil.move(file_path, full_path)

        relative_id = join(random_id, file_name)

        return relative_id, Status.OK, 'File saved successfully'


    def __create_directory(self, random_digits=16) -> Tuple[str, str]:
        """
        Creates a dir with random identifier.

        Parameters
        ------------
        random_digits: int - Represents the number of random digits in the created random id

        Returns
        ------------
        random_id: str - Random generated id.
        full_path: str - Full path to created dir.
        """
        full_path = self.__get_save_path()
        random_str = ''.join(
            random.choices(string.ascii_uppercase + string.digits + string.ascii_lowercase, k=random_digits)
        )
        created_dir = join(full_path, random_str)
        os.makedirs(created_dir)
        return random_str, created_dir

    @staticmethod
    def __get_arq_type(file_path: str) -> str:
        match = re.findall(r"\..*$", file_path)[0]
        return match

    @staticmethod
    def __create_file_name(*identifiers: str):
        return reduce(lambda a, b: a + '_' + b, *identifiers)
