import re
from io import BufferedReader
from typing import Tuple

from flask import Flask, request, send_file
from flask_cors import CORS
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from api.default_service import DefaultService, FileType
from config.config import STREAM_DIR_RELATIVE_PATH
import os

app = Flask(__name__)
CORS(app, resources={r"/storage/*": {"origins": "*"}})
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

    # Get file_name. Not done with BinaryIO
    name = ret.name
    return send_file(name)


@app.delete('/storage/<path:file_path>')
def delete_item(file_path: str):
    service.delete_file(file_path)
    return 'File deleted successfully'


def parse_media_type(media_type: str):
    pattern = re.compile('VIDEO', re.IGNORECASE)
    matches = re.match(pattern, media_type)
    if matches is not None:
        return FileType.VIDEO
    return FileType.FILE


def save_local_file(file_upload: FileStorage, identifiers: str = None):
    file_name = secure_filename(file_upload.filename)
    cwd = os.getcwd()
    relative_path = os.path.join(STREAM_DIR_RELATIVE_PATH, file_name)
    file_path = cwd + relative_path
    file_path = os.path.normpath(file_path)

    file_upload.save(file_path)

    return file_path
