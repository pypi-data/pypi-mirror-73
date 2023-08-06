import json
import os


def initConfig(filename):
    if os.path.exists(filename) is False:
        with open(filename,'w+',encoding='utf-8') as fs:
            fs.write(json.dumps({"m1":"m1"}))
    with open(filename,'r',encoding='utf-8') as fs:
        confistr = fs.read()
    return json.loads(confistr)

ConfigJson=initConfig('jgconfig.json')

if __name__ == '__main__':
    print(ConfigJson)