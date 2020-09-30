import json
import time

from dao.TaskDao import TaskDao
from task.SATask import new_sa_celery_task

def insertNewTask(task_form):
    """
    Create a new task and save the configuration information.
    Parameters:
        task_form: Task information.
    Return: 
        task_form: Response for debug and confirmation;
        task_config: Configure celery tasks;
        status: Success or not
    """
    counter = 0
    task_name = task_form.get('task_name')
    task_config = {}
    task_config['proj_name'] = task_form.get('proj_name')
    task_config['test_var_data_x'] = task_form.get('test_var_data_x')
    task_config['group_var_data_y'] = task_form.get('group_var_data_y')
    task_form['task_config'] = task_config
    
    task_form['task_id'] = 'TASK' + time.strftime('%y%m%d%H%M%S') + '{:02d}'.format(counter)

    if task_name:
        task_form['task_name'] = task_name
    else:
        task_form['task_name'] = task_form['task_id']

    taskDao = TaskDao()
    taskDao.insertNewTask(task_form)

    # create new celery task
    new_sa_celery_task.delay(
        taskid=task_form['task_id'],
        tasktype=task_form['task_type'],
        testvardatax=task_config['test_var_data_x'],
        groupvardatay=task_config['group_var_data_y']
    )
    
    return
