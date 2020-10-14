import pymysql
import json
import sys
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

class Logger(object):
    def __init__(self, fileN='Default.log'):
        self.terminal = sys.stdout
        self.log = open(fileN, 'a')

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        pass

if __name__ == '__main__':
    mysql = MYSQLDB(host="db.neurolearn.com", user="neurolearn", pwd="nl4444_", db="neurolearn")

    sys.stdout = Logger('results.txt') # output console log
    
    # Obtain task ids to show
    task_ids = ['TASK20092101464600']
    # with open('taskids.txt', 'r') as t:
    #     for i in t.readlines():
    #         task_ids.append(i.strip())
    resList = get_results_by_taskids(mysql, task_ids)
    
    # Configure Items to Show
    items = ['Permutation Test p-Value', 'Test Accuracy', 'Test Sensitivity', 'Test Specificity', 'Area Under Curve']
    
    for res in resList:
        print('Task Name: %s' % res[1])
        for itm in items:
            itm_cont = json.loads(res[2])[itm]
            if isinstance(itm_cont, float):
                print('    %s: %.4f' % (itm, itm_cont))
            elif isinstance(itm_cont, str):
                print('    %s: %s' % (itm, itm_cont))
            elif isinstance(itm_cont, list) or isinstance(itm_cont, dict):
                print('    %s: ' % (itm) + str(itm_cont))