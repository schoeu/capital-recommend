from flask import Flask, request
import conf
import recommend
import utils

config = conf.getconfig()

app = Flask(__name__)

@app.route("/")
def hello():
    return "Server is ok."

@app.route("/api/tags")
def tags():
    #recommend.recomm()
    return utils.returnjson('Update tags complete.')

@app.before_request
def checksecretkey():
    secretkey = request.args.get('secretkey')
    if secretkey != config['secretkey']:
        return utils.returnerror('API Forbidden.'), 403
    
app.run(host=config['host'], port=config['port'])