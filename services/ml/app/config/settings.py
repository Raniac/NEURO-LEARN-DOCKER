from flask import Flask
from celery import Celery

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://127.0.0.1:6379/1'
app.config['CELERY_RESULT_BACKEND'] = 'redis://127.0.0.1:6379/1'

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

BASE_URL = "/rest/mlservice"
