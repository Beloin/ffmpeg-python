from enum import Enum
from typing import BinaryIO, List, Dict

import requests

from config.config import STREAM_DIR_RELATIVE_PATH, HLS_DIR_ABS_PATH
from services.file_service import FileService
from services.video_service import VideoService
from storage.driver import DriverInterface
from storage.drivers.filesystem_driver import FileSystemDriver
from redis import Redis
from rq import Queue


class FileType(Enum):
    VIDEO = 'VIDEO'
    FILE = 'FILE'


class DefaultService:

    def __init__(self, redis_queue):
        self._redis_queue = redis_queue
        self.defaultDriver = FileSystemDriver(STREAM_DIR_RELATIVE_PATH)
        self.videoService = VideoService(defaultDriver, HLS_DIR_ABS_PATH)
        self.fileService = FileService(defaultDriver)

    def upload_file(self, path: str, file_type: FileType, notification_url: str,
                    identifiers_list: List[str] = None,
                    identifiers_dict: Dict[str, str] = None
                    ) -> None:
        """
        If sent identifiers list, the dict is ignored.

        First identifier are the most important.
        The last are used to prevent data replacement.
        """

        # Used to sent identifiers to services
        identifiers = []
        # Used to send body into response.
        response_identifiers = {}

        if identifiers_list is not None and len(identifiers_list) > 0:
            for index, value in enumerate(identifiers_list):
                identifiers.append(value)
                response_identifiers[index] = value
        elif identifiers_dict is not None and len(identifiers_dict) > 0:
            for name, value in identifiers_dict.items():
                identifiers.append(value)
                response_identifiers[name] = value

        if file_type == FileType.VIDEO:
            # Enqueue with RedisQueue
            self._redis_queue.enqueue(
                self.videoService.upload, path, *identifiers,
                notification_url=notification_url,
                response_identifiers=response_identifiers,
                on_success=self._on_success_queue
            )
        else:
            # Enqueue with RedisQueue
            self._redis_queue.enqueue(
                self.fileService.upload, path, *identifiers,
                notification_url=notification_url,
                response_identifiers=response_identifiers,
                on_success=self._on_success_queue
            )

    def get_file(self, path: str) -> BinaryIO:
        return self.fileService.download(path)

    def delete_file(self, path: str):
        return self.fileService.delete(path)

    @staticmethod
    def _on_success_queue(job: str, connection: Redis, result: str, *args, **kwargs):
        notification_url = kwargs['notification_url']
        response_identifiers: dict = kwargs['response_identifiers']
        response_identifiers['path'] = result
        print(response_identifiers)

        requests.post(notification_url, json=response_identifiers).json(a=12)
