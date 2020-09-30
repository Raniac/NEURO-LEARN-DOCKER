import json
import pymysql

class Singleton:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(Singleton, cls).__new__(cls)
        return cls._instance

class MySqlDb(Singleton):
    def __init__(self, host, user, pwd, db):
        self.host = host
        self.user = user
        self.pwd = pwd
        self.db = db

    def __getConnect(self):
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

    def execQuery(self, sql):
        """
        Return:
            resList: List of records as tuples of fields.
        """
        cur = self.__getConnect()
        cur.execute(sql)
        resList = cur.fetchall()

        ## Required for query execution
        self.conn.close()
        return resList

    def execNonQuery(self, sql):
        cur = self.__getConnect()
        cur.execute(sql)
        self.conn.commit()
        self.conn.close()
