import json
import os
import requests
import time
import traceback

from pydantic import BaseModel

from config.settings import app
from config.settings import BASE_URL
from config.settings import celery
from service.TaskService import insertNewTask

@app.get("/")
def hello():
    intro_cont = '''
    NEURO-LEARN-DOCKER-SGN(NLD-SGN) is a dockerized application programming
    interface developed with Flask, allowing users to run Schizo_Graph_Net 
    models via the user interface provided by NEURO-LEARN-WEB.
    '''
    return intro_cont

class TaskForm(BaseModel):
    proj_id: str
    proj_name: str
    task_name: str
    task_type: str
    test_var_data_x: list
    group_var_data_y: list

@app.post(BASE_URL + "/v0/task/insert")
async def new_task(task_form: TaskForm):
    response_content = {}

    try:
        insertNewTask(task_form.dict())

        response_content['task_form'] = task_form.dict()
        response_content['msg'] = 'success'
        response_content['code'] = 200

    except:
        response_content['msg'] = traceback.format_exc()[-min(1000, len(traceback.format_exc())):]
        response_content['code'] = 500

    return response_content