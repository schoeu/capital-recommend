import conf
import db
import utils
import json

config = conf.getconfig()

def getcontents():
    sql = 'SELECT topic, content, row_key FROM article_contents where tags IS NULL order by date desc limit {limit}'.format(limit=config['limit'])
    cursor = db.select(sql)
    rs = cursor.fetchall()
    savetags(rs)

def getsigletag(rowkey):
    sql = 'SELECT topic, content, row_key FROM article_contents where row_key = {rowkey} and tags IS NULL limit 1'.format(rowkey=rowkey)
    cursor = db.select(sql)
    rs = cursor.fetchall()
    if len(rs) > 0:
        savetags(rs)

def savetags(rs):
    rowdata = ''
    rowkeys = []
    for i in rs:
        title, content = utils.getalltext(i)
        tags = utils.gettags(title + content)
        rowdata += " WHEN row_key='" + i[2] + "' THEN '" + json.dumps(tags, ensure_ascii=False).replace("'","\'") + "'"
        rowkeys.append("'{key}'".format(key=i[2]))
        print(i[2], i[0])
    if len(rowkeys) > 0:
        sql = "UPDATE article_contents SET tags = CASE {rowdata} END WHERE row_key IN ({rowkeystr})".format(rowdata=rowdata, rowkeystr=','.join(rowkeys))
        db.execute(sql)

def recomm():
    # get contents which analyzed be zero.
    getcontents()

def getarticletag(rowkey):
    sql = "SELECT tags FROM article_contents where row_key = '{}' limit 1".format(rowkey)
    print(sql)
    cursor = db.select(sql)
    rs = cursor.fetchone()
    if rs[0]:
        jsonrs = json.loads(rs[0])
        return jsonrs
    else:
        return []

def getusertag(uid):
    sql = "SELECT tags FROM users where open_id = '{}' limit 1".format(uid)
    print(sql)
    cursor = db.select(sql)
    rs = cursor.fetchone()
    try:
        jsonrs = json.loads(rs[0])
    except:
        return []
    else:
        return jsonrs

def getalltags(atag, utag):
    tmp = {}
    alltags = {}
    atagcopy = atag.copy()
    utagcopy = utag.copy()
    for k in atag:
        for key in utag:
            if k == key:
                num = atag[k] + utag[key]
                tmp[k] = num
                del atagcopy[k]
                del utagcopy[key]
    
    alltags.update(atagcopy)
    alltags.update(utagcopy)
    alltags.update(tmp)
    return alltags

def saveusertag(uid, rs):
    sql = "UPDATE users set tags = '{1}' where open_id = '{0}'".format(uid, rs)
    print('saveusertag', sql)
    db.execute(sql)