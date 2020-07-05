from dao.db import *
import time

def create_new_task(DB, task_form):
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
    try:
        proj_id = task_form['proj_id']
        task_type = task_form['task_type']

        counter = 0
        task_id = 'TASK' + time.strftime('%y%m%d%H%M%S') + '{:02d}'.format(counter)
        task_form['task_id'] = task_id
        print('Creating task: %s' % task_id)
        # app.logger.info('Creating task: %s' % task_id)

        task_name = task_form['task_name']
        task_config = {}
        task_config['proj_name'] = task_form['proj_name']
        task_config['train_data'] = task_form['train_data']
        task_config['val_data'] = task_form['val_data']
        task_config['enable_test'] = task_form['enable_test']
        task_config['test_data'] = task_form['test_data']
        task_config['model'] = task_form['model']
        task_config['param_set'] = task_form['param_set']

        status = insert_new_task(
            mysql=DB,
            task_id=task_id,
            proj_id=proj_id,
            task_name=task_name,
            task_type=task_type,
            task_config=json.dumps(task_config),
            task_status='Submitted'
            )
        if status == 1:
            raise Exception('Database Error!')
        print('Task %s created! Waiting for execution...' % task_id)
        # app.logger.info('Task %s created! Waiting for execution...' % task_id)
        return task_form, task_config, 0
    except Exception as e:
        print(e)
        return None, None, 1