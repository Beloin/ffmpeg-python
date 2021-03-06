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

        If is a dir, returns the path for the `dir`.

        Parameters
        --------
        file_: str | any (as a Buffer like object). Can be a file, or the directory of containing files.
        identifiers: Tuple[str] a list of identifiers, used to identify the path to saved file. The first identifier is used
        as main item e.g. FS: main directory, S3: Bucket Name

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
