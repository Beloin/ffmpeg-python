import os
from dotenv import load_dotenv

APP_ENV = os.environ.get('APP_ENV')

isStaging = APP_ENV == 'staging'
isDevelopment = not isStaging

load_dotenv(f'.env.{APP_ENV}')

STREAM_DIR = os.environ.get('STREAM_DIR')
DRIVER = os.environ.get('DRIVER')

IS_FS = DRIVER == 'FS'
IS_S3 = DRIVER == 'S3'
