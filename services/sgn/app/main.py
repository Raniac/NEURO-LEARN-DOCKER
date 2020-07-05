from flask import Flask, request, jsonify
from celery import Celery
import argparse
import json
import time
import pickle
import traceback

from dao.db import *
from service.task_manipulation_service import *
from sgn import core

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = 'redis://127.0.0.1:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://127.0.0.1:6379/0'
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

def parse_arg():
    parser = argparse.ArgumentParser(description='nld-sgn-main')
    parser.add_argument('--host', dest='host', default='0.0.0.0')
    parser.add_argument('--port', dest='port', default='80')
    parser.add_argument('--db_host', dest='db_host', default='120.79.49.129')
    parser.add_argument('--db_name', dest='db_name', default='neurolearn')
    parser.add_argument('--db_user', dest='db_user', default='neurolearn')
    parser.add_argument('--db_pwd', dest='db_pwd', default='nl4444_')
    args = parser.parse_args()
    return args

DB = init_db(db_host='120.79.49.129', db_name='neurolearn', db_user='neurolearn', db_pwd='nl4444_')

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

@app.route('/api/v0/new_sgn_task', methods=['POST'])
def new_task():
    response_content = {}

    try:
        task_form = json.loads(request.data.decode("utf-8"))

        ## task manipulation service - create a new task
        # DB = init_db(db_host='120.79.49.129', db_name='neurolearn', db_user='neurolearn', db_pwd='nl4444_')
        task_form, task_config, status = create_new_task(DB, task_form)
        if status == 1:
            raise Exception('Database Error!')
        # app.logger.info('Task %s created! Waiting for execution...' % task_id)

        ## let celery worker do the job
        task_executor.delay(
            taskid = task_form['task_id'],
            tasktype = task_form['task_type'],
            traindata = task_config['train_data'],
            valdata = task_config['val_data'],
            enabletest = task_config['enable_test'],
            testdata = task_config['test_data'],
            model = task_config['model'],
            paramset = task_config['param_set']
        )

        response_content['task_form'] = task_form
        response_content['msg'] = 'success'
        response_content['code'] = 200

    except:
        response_content['msg'] = traceback.format_exc()[-min(1000, len(traceback.format_exc())):]
        response_content['code'] = 500

    return jsonify(response_content)

@app.route('/api/v0/test_db', methods=['GET'])
def test_db():
    try:
        # DB = init_db(db_host='120.79.49.129', db_name='neurolearn', db_user='neurolearn', db_pwd='nl4444_')
        fetched = get_data_by_data_name(DB, 'A_181210_140_SZ_sfMRI_AAL90')
        # app.logger.debug(len(fetched))
        return 'success'
    except Exception as e:
        return str(e)

@celery.task
def task_executor(taskid, tasktype, traindata, valdata, enabletest, testdata, model, paramset):
    DB = init_db(db_host='120.79.49.129', db_name='neurolearn', db_user='neurolearn', db_pwd='nl4444_')
    ## data acquisition
    fetched_train_data = []
    for train_data_name in traindata:
        fetched_train_data.append(get_data_by_data_name(DB, train_data_name))
    fetched_val_data = []
    for val_data_name in valdata:
        fetched_val_data.append(get_data_by_data_name(DB, val_data_name))
    
    ## for fine-tune tasks, load saved models from deployed server
    if tasktype == 'dl_ft':
        ## get the model path from database first
        paramset['model_state_path'] = json.loads(get_model_state_by_task_id(DB, paramset['trained_task_id']))['model_state_path']
    
    fetched_test_data = []
    if enabletest:
        for test_data_name in testdata:
            fetched_test_data.append(get_data_by_data_name(DB, test_data_name))
    
    update_task_result_by_task_id(DB, taskid, '', 'Running')
    try:
        ## begin to run model
        results = core.run_model(taskid, tasktype, fetched_train_data, fetched_val_data, enabletest, fetched_test_data, model, paramset)
        results_json = json.dumps(results)
        ## update task results
        update_task_result_by_task_id(DB, taskid, results_json, 'Success')
    except Exception as e:
        traceback.print_exc()
        # update_task_result_by_task_id(DB, taskid, traceback.format_exc()[-min(1000, len(traceback.format_exc())):], 'Failed')
        update_task_result_by_task_id(DB, taskid, e, 'Failed')
    return

if __name__ == "__main__":
    args = parse_arg()
    HOST = args.host
    PORT = int(args.port)
    DB_HOST = args.db_host
    DB_NAME = args.db_name
    DB_USER = args.db_user
    DB_PWD = args.db_pwd
    DB = init_db(db_host=DB_HOST, db_name=DB_NAME, db_user=DB_USER, db_pwd=DB_PWD)
    app.run(host=HOST, port=PORT, debug=True)