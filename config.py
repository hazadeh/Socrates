import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    ELASTICSEARCH_URL = os.environ.get(
        'ES_URL') or 'https://c0e7e39a43aa409d9b05fb1876656f50.us-central1.gcp.cloud.es.io:9243'
    IBM_URL = os.environ.get(
        'IBM_URL') or 'https://api.us-south.natural-language-understanding.watson.cloud.ibm.com/instances/0584cdd7-cf46-4c66-b983-cc18aae2f3ed'
    IBM_API_KEY = os.environ.get('IBM_API_KEY') or ''
    IBM_VERSION = os.environ.get('IBM_VERSION') or '2020-08-01'
