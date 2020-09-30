from fastapi import FastAPI
from celery import Celery

app = FastAPI()

celery = Celery('SATask', broker='redis://127.0.0.1:6379/2')

BASE_URL = "/rest/saservice"