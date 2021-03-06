import json
import time

from dao.TaskDao import TaskDao
from task.MLTask import new_ml_celery_task

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
    task_name = task_form.get('task_name')
    for trans in task_form.get('feat_sel'):
        for estim in task_form.get('estimator'):
            task_config = {}
            task_config['proj_name'] = task_form['proj_name']
            task_config['train_data'] = task_form['train_data']
            task_config['enable_test'] = task_form['enable_test']
            task_config['test_data'] = task_form['test_data']
            task_config['label'] = task_form['label']
            task_config['feat_sel'] = trans
            task_config['estimator'] = estim
            task_config['cv_type'] = task_form['cv_type']
            task_form['task_config'] = task_config
            
            task_form['task_id'] = 'TASK' + time.strftime('%y%m%d%H%M%S') + '{:02d}'.format(counter)

            model_abbrs = {
                'Analysis of Variance': 'anova',
                'Principal Component Analysis': 'pca',
                'Recursive Feature Elimination': 'rfe',
                'None': 'none',
                'Support Vector Machine': 'svm',
                'Random Forest': 'rf',
                'Linear Discriminative Analysis': 'lda',
                'Logistic Regression': 'lr',
                'K Nearest Neighbor': 'knn',
                'Support Vector Regression': 'svr',
                'Elastic Net': 'en',
                'Ordinary Least Square': 'ols',
                'Lasso Regression': 'lasso',
                'Ridge Regression': 'ridge'
            }
            if task_name:
                task_form['task_name'] = task_name + '_' + model_abbrs[trans] + '_' + model_abbrs[estim]
            else:
                task_form['task_name'] = task_form['task_id'] + '_' + model_abbrs[trans] + '_' + model_abbrs[estim]

            taskDao = TaskDao()
            taskDao.insertNewTask(task_form)

            new_ml_celery_task.delay(
                taskid=task_form['task_id'],
                projid=task_form['proj_id'],
                tasktype=task_form['task_type'],
                traindata=task_config['train_data'],
                enabletest=task_config['enable_test'],
                testdata=task_config['test_data'],
                label=task_config['label'],
                featsel=task_config['feat_sel'],
                estimator=task_config['estimator'],
                cv=task_config['cv_type']
            )

            counter += 1
    
    return
