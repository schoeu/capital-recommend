from flask import Flask, request
import conf
import recommend
import utils
import db

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
    secretkey = request.args.get('secretkey')
    rowkey = request.args.get('rowkey')
    if secretkey != config['secretkey'] or not rowkey:
        return utils.returnerror('api error.')
    recommend.getsigletag(rowkey)
    return utils.returnjson('ok.')
    

@app.before_request
def checksecretkey():
    secretkey = request.args.get('secretkey')
    if secretkey != config['secretkey']:
        return utils.returnerror('API Forbidden.'), 403
    
app.run(host=config['host'], port=config['port'])

# finally part.
db.closeconn()