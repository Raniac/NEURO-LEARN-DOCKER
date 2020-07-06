from dao.DB import MySqlDb
from dao.DB import Singleton

class TaskDao(Singleton):
    def __init__(self):
        self.mySqlDb = MySqlDb(
            db_host='120.79.49.129',
            db_name='neurolearn',
            db_user='neurolearn',
            db_pwd='nl4444_'
        )
    
    def insertNewTask(self, task_form):
        sql = """
        INSERT INTO
        backend_submissions
        (`task_id`,
        `proj_id`,
        `task_name`,
        `task_type`,
        `task_config`,
        `task_status`,
        `task_result`)
        VALUES('%s', '%s', '%s', '%s', '%s', '%s', '')
        """ % (task_form['task_id'],
            task_form['proj_id'],
            task_form['task_name'],
            task_form['task_type'],
            task_form['task_config'],
            'Submitted'
        )
        self.mySqlDb.execNonQuery(sql)
        return
    
    def updateTaskResultByTaskId(self, task_id, task_result):
        pass
    
    def getDataByDataName(self, data_name):
        pass
