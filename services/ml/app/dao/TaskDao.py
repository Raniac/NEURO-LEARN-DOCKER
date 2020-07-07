from dao.DB import MySqlDb
from dao.DB import Singleton

class TaskDao(Singleton):
    def __init__(self):
        self.mySqlDb = MySqlDb(
            host='120.79.49.129',
            db='neurolearn',
            user='neurolearn',
            pwd='nl4444_'
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
        """ % (
            task_form['task_id'],
            task_form['proj_id'],
            task_form['task_name'],
            task_form['task_type'],
            task_form['task_config'],
            'Submitted'
        )
        self.mySqlDb.execNonQuery(sql)
        return

    def updateTaskStatusByTaskId(self, task_id, task_status):
        sql = """
        update
        backend_submissions
        set
        task_result = '%s'
        where
        task_id = '%s'
        """ % (
            task_status,
            task_id
        )
        self.mySqlDb.execNonQuery(sql)
        return
    
    def updateTaskResultByTaskId(self, task_id, task_result):
        sql = """
        update
        backend_submissions
        set
        task_status = '%s'
        where
        task_id = '%s'
        """ % (
            task_result,
            task_id
        )
        self.mySqlDb.execNonQuery(sql)
        return
    
    def getDataByDataName(self, data_name):
        sql = """
        select
        data_cont
        from
        backend_datasets
        where
        data_name in %s
        """ % (
            str(tuple(data_name))
        )
        rs = self.mySqlDb.execQuery(sql)
        return rs
