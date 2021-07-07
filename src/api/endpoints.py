import re

from flask import Flask, request
from werkzeug.utils import secure_filename
from api.default_service import DefaultService, FileType
from config.config import STREAM_DIR
import os

app = Flask(__name__)

service = DefaultService()


@app.post('/upload/<path:identifiers>')
def upload_file(identifiers: str):
    """ Identifiers separated by '/'."""
    file = request.files['file']
    file_name = secure_filename(file.filename)
    file_path = os.path.join(STREAM_DIR, file_name)
    file.save(file_path)

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
