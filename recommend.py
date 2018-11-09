import conf
import db
import utils
import json
from math import sqrt

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
        print(title)
        tags = utils.gettags(title + content)
        rowdata += " WHEN row_key='" + i[2] + "' THEN '" + json.dumps(tags, ensure_ascii=False).replace("'","\'") + "'"
        rowkeys.append("'{key}'".format(key=i[2]))
    if len(rowkeys) > 0:
        sql = "UPDATE article_contents SET tags = CASE {rowdata} END WHERE row_key IN ({rowkeystr})".format(rowdata=rowdata, rowkeystr=','.join(rowkeys))
        db.execute(sql)

def recomm():
    # get contents which analyzed be zero.
    getcontents()

def getarticletag(rowkey):
    sql = "SELECT tags FROM article_contents where row_key = '{}' limit 1".format(rowkey)
    cursor = db.select(sql)
    rs = cursor.fetchone()
    if rs[0]:
        jsonrs = json.loads(rs[0])
        return jsonrs
    else:
        return []

def getusertag(uid):
    sql = "SELECT tags FROM users where open_id = '{}' limit 1".format(uid)
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
    db.execute(sql)

def getnewertags(uid):
    sql = 'SELECT row_key, tags FROM article_contents WHERE tags IS NOT NULL ORDER BY date desc limit {limit}'.format(limit=config['limit'])
    cursor = db.select(sql)
    rs = cursor.fetchall()

    usertags = getusertag(uid)
    newusers = fixnums(usertags)
    
    ctt = []
    if len(rs) > 0 and usertags:
        for i in rs:
            utags = i[1]
            if utags:
                newctt = {}
                tagstruct = json.loads(utags)
                for j in tagstruct:
                    newctt[j[0]] = j[1]
                newntags = fixnums(newctt)
                rec = similar_pearson(newusers, newntags)
                if rec > 0 and rec != 1:
                    ctt.append([rec, i[0]])
    ctt.sort(key=lambda k: k[0], reverse=True)
    return ctt

def similar_distance(usertags, newstags):
    si = {}
    for item in newstags:
        if item in usertags:
            si[item] = 1

    if len(si) == 0:
        return 0
    squaressum = sum([pow(usertags[item] - newstags[item], 2) for item in usertags if item in newstags])
    return 1 / (1 + sqrt(squaressum))

def similar_pearson(usertags, newstags):
    si = {}
    for item in usertags:
        if item in newstags:
            si[item] = 1
    
    n = len(si)

    if  n == 0:
        return 1
    
    sum1 = sum([usertags[it] for it in si])
    sum2 = sum([newstags[it] for it in si])

    sum1Sq = sum([pow(usertags[it], 2) for it in si])
    sum2Sq = sum([pow(newstags[it], 2) for it in si])

    pSum = sum([usertags[it] * newstags[it] for it in si])

    num = pSum - (sum1 * sum2 / n)
    den = sqrt((sum1Sq - pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))
    if den == 0:
        return 0
    
    r = num / den
    return r

def fixnums(rs):
    ctt = {}
    for i in rs:
        ctt[i] = rs[i] * 100
    return ctt