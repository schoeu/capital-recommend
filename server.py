from flask import Flask, request
import conf
import recommend
import utils
import db
import json

config = conf.getconfig()

app = Flask(__name__)

@app.route("/")
def hello():
    return "Server is ok."

@app.route("/api/tags")
def tags():
    recommend.recomm()
    return utils.returnjson('Update tags complete.')

@app.route("/api/sigletags")
def sigletags():
    rowkey = request.args.get('rowkey')
    if not rowkey:
        return utils.returnerror('api error.')
    recommend.getsigletag(rowkey)
    return utils.returnjson('ok.')

@app.route("/api/usertags")
def usertags():
    rowkey = request.args.get('rowkey')
    uid = request.args.get('uid')
    if uid and rowkey:
        articletag = recommend.getarticletag(rowkey)
        usertag = recommend.getusertag(uid)

        atag = dict(articletag)
        utag = dict(usertag)
        alltags = recommend.getalltags(atag, utag)
        
        print(alltags)
        recommend.saveusertag(uid, json.dumps(alltags, ensure_ascii=False))
        return utils.returnjson('Update user tags complete.')
    else:
        return utils.returnerror('Need uid and rowkey params.')
    

@app.before_request
def checksecretkey():
    secretkey = request.args.get('secretkey')
    if secretkey != config['secretkey']:
        return utils.returnerror('API Forbidden.'), 403
    
app.run(host=config['host'], port=config['port'])

# finally part.
db.closeconn()