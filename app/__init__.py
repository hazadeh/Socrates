from flask import Flask
from config import Config
from flask_bootstrap import Bootstrap
from elasticsearch import Elasticsearch


app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)

from app import routes

app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) if app.config['ELASTICSEARCH_URL'] else None
