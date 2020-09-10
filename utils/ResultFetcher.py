import pymysql
import json
import traceback

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

def get_results_by_taskids(mysql, task_ids):
    try:
        sql = """
        SELECT task_id, task_result
        FROM backend_submissions as submissions
        WHERE submissions.task_id in (%s)
        """ % (','.join(list(map(lambda x: "'" + x + "'", task_ids))))
        fetList = mysql.ExecQuery(sql)
        return fetList
    except Exception as e:
        traceback.print_exc()

if __name__ == '__main__':
    mysql = MYSQLDB(host="db.neurolearn.com", user="neurolearn", pwd="nl4444_", db="neurolearn")
    resList = get_results_by_taskids(mysql, ['TASK20080706524300', 'TASK20091002390308'])
    print(json.loads(resList[0][1]))