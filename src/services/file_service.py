from typing import Union, BinaryIO

from storage.driver import Status
from .file_service_interface import (
    FileServiceInterface,
    DriverInterface,
    DriverException
)
from services.null_identifiers import NullIdentifiers


class FileService(FileServiceInterface):
    def __init__(self, driver: DriverInterface) -> None:
        super().__init__(driver)

    def upload(self, file: Union[str, any], *identifiers: str) -> str:
        path, status, info = self.driver.upload_file(file, *identifiers)
        if type(file) is not str: raise NotImplementedError
        if identifiers is None or len(identifiers) == 0:
            raise NullIdentifiers()

        if status == Status.FAIL:
            raise DriverException(info)

        return path

    def download(self, path: str) -> BinaryIO:
        file, status, info = self.driver.download_file(path)

        if status == Status.FAIL:
            raise DriverException(info)

        return file

    def delete(self, path: str) -> Union[None, bool]:
        status, info = self.driver.delete_file(path)

        if status == Status.FAIL:
            raise DriverException(info)

        return True
