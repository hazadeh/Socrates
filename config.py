import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    ELASTICSEARCH_URL = os.environ.get('ES_URL') or ''
    IBM_URL = os.environ.get('IBM_URL') or ''
    IBM_API_KEY = os.environ.get('IBM_API_KEY') or ''
    IBM_VERSION = os.environ.get('IBM_VERSION') or '2018-03-16'

