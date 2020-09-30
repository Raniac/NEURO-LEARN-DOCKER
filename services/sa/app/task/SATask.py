from celery import Celery
import pandas as pd
import traceback
import json

from config.settings import celery
from dao.TaskDao import TaskDao
from task.Core import test_sa_task

@celery.task(soft_time_limit=1e3)
def new_sa_celery_task(taskid, tasktype, testvardatax, groupvardatay):
    taskDao = TaskDao()
    taskDao.updateTaskStatusByTaskId(task_id=taskid, task_status='Running')
    try:
        testvardatax_queryset = taskDao.getDataByDataName(data_name=testvardatax)
        testvardatax_list = []
        for itm in list(testvardatax_queryset):
            testvardatax_list.append(pd.read_json(itm[0]))

        groupvardatay_list = []
        groupvardatay_queryset = taskDao.getDataByDataName(data_name=groupvardatay)
        for jtm in list(groupvardatay_queryset):
            groupvardatay_list.append(pd.read_json(jtm[0]))

        results = test_sa_task(taskid, tasktype, testvardatax_list, groupvardatay_list)
        taskDao.updateTaskStatusByTaskId(task_id=taskid, task_status='Finished')
        taskDao.updateTaskResultByTaskId(task_id=taskid, task_result=json.dumps(results))
    except Exception as e:
        traceback.print_exc()
        taskDao.updateTaskStatusByTaskId(task_id=taskid, task_status='Failed')
        taskDao.updateTaskResultByTaskId(task_id=taskid, task_result=json.dumps(str(e)))
    return