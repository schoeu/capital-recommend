import conf
import db

config = conf.getconfig()

def getcontents():
    sql = 'SELECT topic, content FROM capital.article_contents where analyzed = 0 order by date desc limit 500;'
    cursor = db.select(sql)
    rs = cursor.fetchall()
    ids = [i[0] for i in rs]

# main
def main():
    # get contents which analyzed be zero.
    getcontents()

    # finally
    db.closeconn()

if __name__ == '__main__':
    main()