import jieba.analyse
import json
import conf

config = conf.getconfig()

def getalltext(data):
    if len(data) > 0:
        title = data[0]
        content = ''
        textdata = json.loads(data[1])
        for i in textdata:
            if i['name'] == 'text':
                content += i['content']
    return title, content

def gettags(data):
    allowpos = tuple(config['allowpos'])
    tags = jieba.analyse.extract_tags(data, topK=config['topkey'], withWeight=True, allowPOS=allowpos)
    return tags