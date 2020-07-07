import argparse
import json
import pickle
import time
import traceback

from flask import Flask, request, jsonify
from celery import Celery

from service.TaskService import insertNewTask

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://127.0.0.1:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://127.0.0.1:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

BASEURL = "/rest/mlservice"

def parse_arg():
    parser = argparse.ArgumentParser(description='nls-ml-main')
    parser.add_argument('--host', dest='host', default='0.0.0.0')
    parser.add_argument('--port', dest='port', default='80')
    parser.add_argument('--db_host', dest='db_host', default='120.79.49.129')
    parser.add_argument('--db_name', dest='db_name', default='neurolearn')
    parser.add_argument('--db_user', dest='db_user', default='neurolearn')
    parser.add_argument('--db_pwd', dest='db_pwd', default='nl4444_')
    args = parser.parse_args()
    return args

## Loggers
# app.logger.debug('A value for debugging')
# app.logger.info('An info for notice')
# app.logger.warning('A warning occurred (%d apples)', 42)
# app.logger.error('An error occurred')

@app.route('/')
def intro():
    intro_cont = '''
    NEURO-LEARN-DOCKER-SGN(NLD-SGN) is a dockerized application programming
    interface developed with Flask, allowing users to run Schizo_Graph_Net 
    models via the user interface provided by NEURO-LEARN-WEB.
    '''
    return intro_cont

@app.route(BASEURL + '/v0/task/insert', methods=['POST'])
def new_task():
    response_content = {}

    try:
        task_form = json.loads(request.data.decode("utf-8"))
        insertNewTask(task_form)

        response_content['task_form'] = task_form
        response_content['msg'] = 'success'
        response_content['code'] = 200

    except:
        response_content['msg'] = traceback.format_exc()[-min(1000, len(traceback.format_exc())):]
        response_content['code'] = 500

    return jsonify(response_content)

@app.route(BASEURL + '/v0/healthcheck', methods=['GET'])
def test_db():
    try:
        return 'success'
    except Exception as e:
        return str(e)

import json
import traceback

import pandas as pd

from dao.TaskDao import TaskDao
from task.Core import ml_task

@celery.task
def new_ml_celery_task(taskid, tasktype, traindata, enabletest, testdata, label, featsel, estimator, cv):
    taskDao = TaskDao()
    taskDao.updateTaskStatusByTaskId(task_id=taskid, task_status='Running')
    try:
        train_data_queryset = taskDao.getDataByDataName(data_name=traindata)
        train_data_list = []
        for itm in list(train_data_queryset):
            train_data_list.append(pd.read_json(itm[0]))

        test_data_list = []
        if enabletest:
            test_data_queryset = taskDao.getDataByDataName(data_name=testdata)
            for jtm in list(test_data_queryset):
                test_data_list.append(pd.read_json(jtm[0]))

        results = ml_task(taskid, tasktype, train_data_list, enabletest, test_data_list, label, featsel, estimator, cv)
        results_json = json.dumps(results)
        taskDao.updateTaskStatusByTaskId(task_id=taskid, task_status='Finished')
        taskDao.updateTaskResultByTaskId(task_id=taskid, task_result=results_json)
    except Exception as e:
        traceback.print_exc()
        taskDao.updateTaskStatusByTaskId(task_id=taskid, task_status='Failed')
        taskDao.updateTaskResultByTaskId(task_id=taskid, task_result=traceback.format_exc()[-min(1000, len(traceback.format_exc())):])
    return