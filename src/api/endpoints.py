from flask import Flask, request
from werkzeug.utils import secure_filename
from api.default_service import DefaultService
from config.config import STREAM_DIR
import os

app = Flask(__name__)

service = DefaultService()


@app.post('/upload/<path:identifiers>')
def upload_file(identifiers: str):
    file = request.files['file']
    file_name = secure_filename(file.filename)
    file_path = os.path.join(STREAM_DIR, file_name)
    path = file.save(file_path)

    path = service.upload_file(*identifiers)
    return path


@app.get('/storage/<path:file_path>',)
def get_file(file_path: str):
    return service.get_file(file_path)


@app.delete('/storage/<path:file_path>')
def delete_item(file_path: str):
    return service.delete_file(file_path)
