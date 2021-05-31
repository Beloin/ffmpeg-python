import os

APP_ENV = os.environ.get('APP_ENV')

isStaging = APP_ENV == 'staging'
isDevelopment = not isStaging
