import json
import os
import requests
import time
import traceback

from config.settings import app
from config.settings import BASE_URL

@app.get("/")
def hello():
    return "Hello FastAPI!"