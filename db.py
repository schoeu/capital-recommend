import pymysql 
import os
import conf
from DBUtils.PooledDB import PooledDB,SharedDBConnection


config = conf.getconfig()
dbinfo = config['db']
# conn = pymysql.connect(dbinfo['host'], dbinfo['user'], dbinfo['password'], dbinfo['dbname'], charset='utf8')

pool = PooledDB(
    creator = pymysql,
    maxconnections = 0,
    mincached = 0,
    maxshared = 3,
    blocking = True,
    setsession = [],
    ping = 0,
    host = dbinfo['host'],
    user = dbinfo['user'],
    password = dbinfo['password'],
    database = dbinfo['dbname'],
    charset = 'utf8'
)
conn = pool.connection()
cursor = conn.cursor()

def executemany(str, data):
    getconn()
    # cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        cursor.executemany(str, data)
        # data = cursor.fetchone()
        conn.commit()
    except Exception as e:
        print('executemany err: ' ,e)
        conn.rollback()
    closeconn()

def select(str):
    getconn()
    try:
        cursor.execute(str)
    except Exception as e:
        print('select sql err: ', e)
    return cursor

def selectall(str):
    getconn()
    try:
        cursor.execute(str)
        r = cursor.fetchall()
        return r
    except Exception as e:
        print('selectall sql err: ', e)
    closeconn()
   

def selectone(str):
    getconn()
    try:
        cursor.execute(str)
        r = cursor.fetchone()
        return r
    except Exception as e:
        print('selectone sql err: ', e)
    closeconn()

def closeconn():
    global cursor, conn
    cursor.close()
    # close conn
    conn.close()

def execute(str):
    getconn()
    try:
        # 执行SQL语句
        cursor.execute(str)
        # 提交到数据库执行
        conn.commit()
    except Exception as e:
        # 发生错误时回滚
        conn.rollback()
        print('Execute sql err: ', e)
    closeconn()

def getconn():
    global cursor, conn
    conn = pool.connection()
    cursor = conn.cursor()



 
# conn = pool.connection()  #以后每次需要数据库连接就是用connection（）函数获取连接就好了
# cur=conn.cursor()
# SQL="select * from table1"
# r=cur.execute(SQL)
# r=cur.fetchall()
# cur.close()
# conn.close()