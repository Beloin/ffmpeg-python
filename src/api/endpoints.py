from flask import Flask, request

from services.file_service import FileService
from services.video_service import VideoService

app = Flask(__name__)

defaulDriver = None
videoService = VideoService(defaulDriver)
fileService = FileService(defaulDriver)


@app.get('/storage/<path:file_path>',)
def get_file(file_path: str):

    return f'Getting... {file_path}'


@app.post('/upload/<path:identifiers>')
def upload_file(identifiers: str):
    """
    Identifiers separeted by '/'.
    """

    return 'Uploading...'


@app.delete('/storage/<path:file_path>')
def delete_item(file_path: str):

    return 'Deleting...'
