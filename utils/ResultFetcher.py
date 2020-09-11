import pymysql
import json
import traceback

class MYSQLDB():
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

def get_results_by_taskids(mysql, task_ids):
    try:
        sql = """
        SELECT task_id, task_name, task_result
        FROM backend_submissions as submissions
        WHERE submissions.task_id in (%s)
        """ % (','.join(list(map(lambda x: "'" + x + "'", task_ids))))
        fetList = mysql.ExecQuery(sql)
        return fetList
    except:
        traceback.print_exc()

if __name__ == '__main__':
    mysql = MYSQLDB(host="db.neurolearn.com", user="neurolearn", pwd="nl4444_", db="neurolearn")
    task_ids = []
    with open('cache.txt', 'r') as t:
        for i in t.readlines():
            task_ids.append(i.strip())
    resList = get_results_by_taskids(mysql, task_ids)
    
    # Configure Items to Show
    items = ['Optimal CV Accuracy', 'Test Accuracy', 'Area Under Curve']
    
    for res in resList:
        print('Task Name: %s' % res[1])
        for itm in items:
            print('    %s: %.4f' % (itm, json.loads(res[2])[itm]))