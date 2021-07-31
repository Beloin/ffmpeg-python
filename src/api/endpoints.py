import re
from typing import Tuple

from flask import Flask, request
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from api.default_service import DefaultService, FileType
from config.config import STREAM_DIR
import os

app = Flask(__name__)

service = DefaultService()


@app.post('/storage/<path:identifiers>')
def upload_file(identifiers: str):
    """ Identifiers separated by '/'."""
    file_upload = request.files['file']
    file_path = save_local_file(file_upload)

    request_dict = request.form.to_dict()
    file_type = parse_media_type(request_dict["mediaType"])

    path = service.upload_file(file_path, file_type, *identifiers.split('/'))

    return path


@app.get('/storage/<path:file_path>')
def get_file(file_path: str):
    ret = service.get_file(file_path)
    return ret.read()


@app.delete('/storage/<path:file_path>')
def delete_item(file_path: str):
    return service.delete_file(file_path)


def parse_media_type(media_type: str):
    if re.match("/VIDEO/gi", media_type):
        return FileType.VIDEO
    return FileType.FILE


def save_local_file(file_upload: FileStorage, identifiers: str = None):
    file_name = secure_filename(file_upload.filename)
    cwd = os.getcwd()
    relative_path = os.path.join(STREAM_DIR, file_name)
    file_path = cwd + relative_path

    file_upload.save(file_path)

    return file_path
