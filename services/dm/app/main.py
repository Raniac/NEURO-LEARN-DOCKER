import json
import os
import requests
import time
import traceback

from fastapi import File, UploadFile

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

# Refer to https://www.jianshu.com/p/56179dcfec4e
@app.post(BASE_URL + "/v0/hdfs/upload")
def uploadFile(file: UploadFile = File(...)):
    res = fromLocalToHdfs(file)
    return res

def fromLocalToHdfs(f: UploadFile = File(...)):
    response = {}
    try:
        if not os.path.exists('tmp'):
            os.mkdir('tmp')
        file_name = 'tmp/' + str(f.filename)
        with open(file_name, 'wb+') as dest:
            dest.write(f.file.read())
        
        client.makedirs("/test_data")
        client.upload("/test_data", file_name)

        response['code'] = 0
        response['status'] = 'success'
    
    except Exception as e:
        traceback.print_exc()
        response['code'] = 1
        response['status'] = 'failure'
        response['message'] = str(e)
    
    return json.dumps(response)