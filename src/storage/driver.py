import abc
from enum import Enum
from typing import Literal, Tuple, Union, BinaryIO


class Status(Enum):
    OK = 'OK'
    FAIL = 'FAIL'


class DriverInterface(metaclass=abc.ABCMeta):
    """
    Driver interface.
    """

    @abc.abstractmethod
    def upload_file(self, file_: Union[str, any], *identifiers: str, file_name: str = None) -> Tuple[str, Status, str]:
        """ 
        Uploads a file. or a dir. 

        Parameters
        --------
        file_: str | any (as a Buffer like object). Can be file or the directory of containing files.
        identifiers: Tuple[str]

        file_name: str represents the file_name. (Optional)
        If sent `file_name` the last identifier is not used anymore for identify the file.

        Returns
        --------
        Tuple containing:
        path: str
        status: Status
        info: str
        """

        raise NotImplementedError

    @abc.abstractmethod
    def download_file(self, path: str) -> Tuple[Union[BinaryIO, any], Status, str]:
        """
        Downloads a file.

        Parameters
        ----
        path: str

        Returns
        ----
        Tuple containing:
        file: any
        status: Status,
        info: str
        """

        raise NotImplementedError

    @abc.abstractmethod
    def delete_file(self, path: str) -> Tuple[Status, str]:
        """
        Deletes a file.

        Parameters
        ----
        path: str

        Returns
        ----
        Tuple containing:
        status: Status,
        info: str
        """

        raise NotImplementedError
