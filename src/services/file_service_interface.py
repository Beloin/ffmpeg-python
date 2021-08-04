import abc
from typing import Union
from storage.driver import DriverInterface


class DriverException(Exception):
    """ Raised when driver fails to upload. """

    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class FileServiceInterface(metaclass=abc.ABCMeta):
    """
    FileServiceInterface. Used to access or upload a file.
    """

    def __init__(self, driver: DriverInterface) -> None:
        self.driver = driver

    @abc.abstractmethod
    def upload(self, file: Union[str, any], *identifiers: str) -> str:
        r"""
        Upload file method.

        :param file: Path for the current file.
        :param identifiers: a list of identifiers passed to Driver
        """
        raise NotImplementedError

    @abc.abstractmethod
    def download(self, path: str) -> any:
        raise NotImplementedError

    @abc.abstractmethod
    def delete(self, path: str) -> Union[None, bool]:
        raise NotImplementedError
