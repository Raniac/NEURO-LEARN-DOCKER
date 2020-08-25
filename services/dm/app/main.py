from config.settings import app
from config.settings import BASE_URL
from config.settings import client

@app.get("/")
def hello():
    return "Hello FastAPI!"

@app.get(BASE_URL + "/v0/hdfs/status")
def getHdfsStatus():
    status = client.status("/")
    return status