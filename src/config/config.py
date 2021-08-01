import os
from os.path import join, normpath

from dotenv import load_dotenv

APP_ENV = os.environ.get('APP_ENV')

isStaging = APP_ENV == 'staging'
isDevelopment = not isStaging

load_dotenv(f'.env.{APP_ENV}')

RABBITMQ_URL = os.environ.get('RABBITMQ_URL') or 'ampq://localhost'

STREAM_DIR_RELATIVE_PATH = os.environ.get('STREAM_DIR')
HLS_DIR_RELATIVE_PATH = os.environ.get('HLS_DIR')

# HLS DIR ABS PATH.
HLS_DIR_ABS_PATH = normpath(os.getcwd() + HLS_DIR_RELATIVE_PATH)
STREAM_DIR_ABS_PATH = normpath(os.getcwd() + STREAM_DIR_RELATIVE_PATH)

DRIVER = os.environ.get('DRIVER')

IS_FS = DRIVER == 'FS'
IS_S3 = DRIVER == 'S3'
