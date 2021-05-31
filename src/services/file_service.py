from typing import Union
from .file_service_interface import (
    FileServiceInterface,
    DriverInterface,
    DriverException
)


class FileService(FileServiceInterface):
    def __init__(self, driver: DriverInterface) -> None:
        super().__init__(driver)

    def upload(self, file: Union[str, any], *identifiers: str) -> str:
        path, status, info = self.driver.upload_file(file, *identifiers)

        if status == 'FAIL':
            raise DriverException(info)

        return path

    def donwload(self, path: str) -> any:
        file, status, info = self.driver.download(path)

        if status == 'FAIL':
            raise DriverException(info)

        return file

    def delete(self, path: str) -> Union[None, bool]:
        status, info = self.driver.delete_file(path)

        if status == 'FAIL':
            raise DriverException(info)

        
