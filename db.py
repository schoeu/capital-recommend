import pymysql 
import os
import conf

config = conf.getconfig()
dbinfo = config['db']
conn = pymysql.connect(dbinfo['host'], dbinfo['user'], dbinfo['password'], dbinfo['dbname'], charset='utf8')
cursor = conn.cursor()

def executemany(str, data):
    # cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        cursor.executemany(str, data)
        # data = cursor.fetchone()
        conn.commit()
    except Exception as e:
        print('Sql err: ' ,e)
        conn.rollback()

def select(str):
    try:
        cursor.execute(str)
    except Exception as e:
        print('Select sql err: ', e)
    return cursor

def closeconn():
    cursor.close()
     # close conn
    conn.close()

def execute(str):
    try:
        # 执行SQL语句
        cursor.execute(str)
        # 提交到数据库执行
        conn.commit()
    except Exception as e:
        # 发生错误时回滚
        conn.rollback()
        print('Execute sql err: ', e)

    