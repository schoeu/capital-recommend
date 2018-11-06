import conf
import db
import utils
import json

config = conf.getconfig()

def getcontents():
    sql = 'SELECT topic, content, row_key FROM article_contents where tags IS NULL order by date desc limit {limit}'.format(limit=config['limit'])
    cursor = db.select(sql)
    rs = cursor.fetchall()
    rowdata = ''
    rowkeys = []
    for i in rs:
        title, content = utils.getalltext(i)
        tags = utils.gettags(title + content)
        rowdata += " WHEN row_key='" + i[2] + "' THEN '" + json.dumps(tags, ensure_ascii=False).replace("'","\'") + "'"
        rowkeys.append("'{key}'".format(key=i[2]))
        print(i[2], i[0])
    if len(rowkeys) > 0:
        savetags(rowdata, rowkeys)

def savetags(data, rowkeys):
    sql = "UPDATE article_contents SET tags = CASE {rowdata} END WHERE row_key IN ({rowkeystr})".format(rowdata=data, rowkeystr=','.join(rowkeys))
    db.execute(sql)

def recomm():
    # get contents which analyzed be zero.
    getcontents()

    # finally part.
    db.closeconn()
