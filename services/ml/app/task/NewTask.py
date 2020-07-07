import json
import traceback

from celery import Celery
import pandas as pd

from dao.TaskDao import TaskDao
from task.Core import ml_task

celery = Celery(broker='redis://127.0.0.1:6379/0')

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
        taskDao.updateTaskStatusByTaskId(task_id=taskid, task_status='Finished')
        taskDao.updateTaskResultByTaskId(task_id=taskid, task_result=json.dumps(results))
    except:
        traceback.print_exc()
        taskDao.updateTaskStatusByTaskId(task_id=taskid, task_status='Failed')
        taskDao.updateTaskResultByTaskId(task_id=taskid, task_result=json.dumps(traceback.format_exc()[-min(1000, len(traceback.format_exc())):]))
    return
