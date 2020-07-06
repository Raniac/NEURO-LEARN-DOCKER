import json
import time

from celery import Celery

from dao.TaskDao import TaskDao
from task.NewTask import new_ml_celery_task

def insertNewTask(task_form):
    """
    Create a new task and save the configuration information.
    Parameters:
        DB: Database object for DAO;
        task_form: Task information.
    Return: 
        task_form: Response for debug and confirmation;
        task_config: Configure celery tasks;
        status: Success or not
    """
    counter = 0
    task_form['task_id'] = 'TASK' + time.strftime('%y%m%d%H%M%S') + '{:02d}'.format(counter)
    
    task_config = {}
    task_config['proj_name'] = task_form['proj_name']
    task_config['train_data'] = task_form['train_data']
    task_config['val_data'] = task_form['val_data']
    task_config['enable_test'] = task_form['enable_test']
    task_config['test_data'] = task_form['test_data']
    task_config['model'] = task_form['model']
    task_config['param_set'] = task_form['param_set']
    task_form['task_config'] = task_config

    taskDao = TaskDao()
    taskDao.insertNewTask(task_form)

    new_ml_celery_task.delay(task_form)
    
    return
