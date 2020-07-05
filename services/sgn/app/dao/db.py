import pymysql
import json

## TODO modify MYSQLDB as singleton class
class Singleton:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

class MYSQLDB(Singleton):
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __GetConnect(self):
        try:
            self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.pwd,
                database=self.db,
                charset="utf8"
                )
            cur = self.conn.cursor()
            return cur
        except Exception as e:
            print('Fail connection: ', e)

    def ExecQuery(self, sql):
        """
        Return:
            resList: List of records as tuples of fields.
        """
        cur = self.__GetConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        ## Required for query execution
        self.conn.close()
        return resList

    def ExecNonQuery(self, sql):
        cur = self.__GetConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()

def init_db(db_host, db_name, db_user, db_pwd):
    mysql = MYSQLDB(host=db_host, db=db_name, user=db_user, pwd=db_pwd)
    return mysql

def insert_new_task(mysql, task_id, proj_id, task_name, task_type, task_config, task_status):
    try:
        sql = """
        INSERT INTO backend_submissions(`task_id`, `proj_id`, `task_name`, `task_type`, `task_config`, `task_status`, `task_result`)
        VALUES('%s', '%s', '%s', '%s', '%s', '%s', '')
        """ % (task_id, proj_id, task_name, task_type, task_config, task_status)
        mysql.ExecNonQuery(sql)
        status = 0
    except Exception as e:
        print(e)
        status = 1
    return status

def update_task_result_by_task_id(mysql, task_id, task_result, task_status):
    try:
        sql = """
        UPDATE backend_submissions
        SET `task_result` = '%s', `task_status` = '%s'
        WHERE `task_id` = '%s'
        """ % (task_result, task_status, task_id)
        mysql.ExecNonQuery(sql)
    except Exception as e:
        print(e)
    return

# def insert_new_model_with_task_id(mysql, task_id, model_path):
#     try:
#         sql = """
#         INSERT INTO backend_models(`model_name`, `model_path`)
#         VALUES('%s', '%s')
#         """ % (task_id, model_path)
#         mysql.ExecNonQuery(sql)
#         status = 0
#     except Exception as e:
#         print(e)
#         status = 1
#     return status

def get_data_by_data_name(mysql, data_name):
    try:
        sql = """
        SELECT data_cont
        FROM backend_datasets as datasets
        WHERE datasets.data_name = '%s'
        """ % (data_name)
        fetList = mysql.ExecQuery(sql)
        return fetList
    except Exception as e:
        return e

def get_model_state_by_task_id(mysql, task_id):
    try:
        sql = """
        SELECT task_result
        FROM backend_submissions as submissions
        WHERE submissions.task_id = '%s'
        """ % (task_id)
        fetList = mysql.ExecQuery(sql)
        return fetList[0][0]
    except Exception as e:
        return e

if __name__ == '__main__':
    mysql = MYSQLDB(host="120.79.49.129", user="root", pwd="root", db="neurolearn")
    resList = get_model_state_by_task_id(mysql, 'TASK20012911464300')
    print(json.loads(resList)['model_state_path'])