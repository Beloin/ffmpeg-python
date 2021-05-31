import abc
from typing import Literal, Tuple, Union

Status = Literal['OK', 'FAIL']


class DriverInterface(metaclass=abc.ABCMeta):
    """
    Driver interface.
    """

    @abc.abstractmethod
    def upload_file(self, file: Union[str, any], *identifiers: str) -> Tuple[str, Status, str]:
        """ 
        Uploads a file. or a dir. 

        Parameters
        --------
        file: str | any (as a Buffer like object)
        identifiers: Tuple[str]

        Returns
        --------
        Tuple containing:
        path: str
        status: Status
        info: str
        """

        raise NotImplementedError

    @abc.abstractmethod
    def download_file(self, path: str) -> Tuple[any, Status, str]:
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
        file: any
        status: Status,
        info: str
        """

        raise NotImplementedError
