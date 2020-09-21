import json
import traceback

from celery import Celery
from flask import Flask
import pandas as pd

from config.settings import celery
from dao.TaskDao import TaskDao
from task.Core import ml_task

@celery.task(soft_time_limit=4e4)
def new_ml_celery_task(taskid, projid, tasktype, traindata, enabletest, testdata, label, featsel, estimator, cv):
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

        results = ml_task(taskid, projid, tasktype, train_data_list, enabletest, test_data_list, label, featsel, estimator, cv)
        taskDao.updateTaskStatusByTaskId(task_id=taskid, task_status='Finished')
        taskDao.updateTaskResultByTaskId(task_id=taskid, task_result=json.dumps(results))
    except Exception as e:
        traceback.print_exc()
        taskDao.updateTaskStatusByTaskId(task_id=taskid, task_status='Failed')
        taskDao.updateTaskResultByTaskId(task_id=taskid, task_result=json.dumps(str(e)))
    return
