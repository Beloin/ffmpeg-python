from io import BufferedReader
import os
from os.path import join, normpath, isfile
import shutil
from typing import Tuple, Union
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

    def upload_file(self, file_or_dir: Union[str, any], *identifiers: str, file_name: str = None) -> Tuple[
        Union[str, None], Status, str
    ]:
        # to_save = self.__join_cwd(self.save_dir, *identifiers)

        if type(file_or_dir) is str:
            try:
                return self.__save_file(file_name, file_or_dir, identifiers)
            except Exception as e:
                return None, Status.FAIL, str(e)

        # If is not file. We don't have yet an implementation.
        raise Exception('File not sent in str like.')

    def __save_file(self, file_name, file_, identifiers):
        to_path = self.__create_dir(*identifiers, file_name=file_name)
        shutil.move(file_, to_path)
        return to_path, Status.OK, 'File saved successfully'

    def delete_file(self, path: str) -> Tuple[Status, str]:
        try:
            path = self.__normajoin(self.save_dir, path)
            os.remove(path)

            return Status.OK, 'File deleted successfully'
        except Exception as e:
            return Status.FAIL, str(e)

    def download_file(self, path: str) -> Tuple[any, Status, str]:
        try:
            reader = self.__read_file(path)
            return reader, Status.OK, 'File sent in Buffer.'
        except Exception as e:
            return None, Status.FAIL, str(e)

    # Private Methods
    @staticmethod
    def __read_file(path: str) -> BufferedReader:
        if not isfile(path):
            raise Exception('Path needs to be a file.')
        f = open(path, 'rb')

        return f

    @staticmethod
    def __normajoin(*paths: str):
        return normpath(join(*paths))

    @staticmethod
    def __join_cwd(*paths: str):
        cwd = os.getcwd()
        path = join(*paths)
        return cwd + path

    # def __create_dir(self, *identifiers: str, file_name: str = None) -> str:
    #     """
    #     If `file_name` is None, last id is used as file_name.
    #
    #     Returns
    #     --------
    #     path to file. (obs: File is not created.)
    #     """
    #
    #     if file_name:
    #         path = self.__normajoin(*identifiers)
    #         return self.__normajoin(path, file_name)
    #
    #     file = identifiers[len(identifiers) - 1]
    #     dirs = identifiers[:len(identifiers) - 1]
    #
    #     path = self.__normajoin(self.save_dir, *dirs)
    #     os.makedirs(path)
    #
    #     return self.__normajoin(path, *file)

    def __create_dir(self, *identifiers: str, file_name: str = None) -> str:
        """
        Creates a dir with the identifiers and return path to *file*.

        If `file_name` is None, last id is used as file_name.

        IMPORTANT : Returns path to save *file* which means the current returned file does not exist.

        Returns
        --------
        path to file. (obs: File is not created.)
        """

        if file_name:
            path = join(*identifiers)
            path = self.__join_cwd(path)
            os.makedirs(path)

            path = join(path, file_name)

            return path

        file_name = identifiers[len(identifiers) - 1]
        dirs = identifiers[:len(identifiers) - 1]

        path = join(self.save_dir, *dirs)
        path = self.__join_cwd(path)
        os.makedirs(path)

        return join(path, *file_name)
