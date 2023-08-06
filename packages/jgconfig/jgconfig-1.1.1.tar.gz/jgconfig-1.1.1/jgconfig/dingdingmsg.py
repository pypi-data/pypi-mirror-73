
import requests
import config
import datetime


class DingDingPush:
    dingdingpushURL = ''
    DDPASS='运维'

    @staticmethod
    def pushMsg(msgs,isAtAll=True) -> str:
        inow = datetime.datetime.now()
        jsonReq = {
            "msgtype": "text", 
            "text": {
                "content": f'{DingDingPush.DDPASS}:[{inow}] <br/>' + msgs
            }, 
            "at": {
                # "atMobiles": [
                #     "156xxxx8827", 
                #     "189xxxx8325"
                # ], 
                "isAtAll": isAtAll
            }
        }

        bak = requests.post(DingDingPush.dingdingpushURL,json=jsonReq )
        return bak

    def __init__(self):
        self.msgs = ''

    def addmd(self,msg):
        self.msgs = self.msgs + msg + '\n'

    def pushmd(self) -> (str, str):

        jsonReq = {
            "msgtype": "markdown",
            "markdown": {
                "title":f"{DingDingPush.DDPASS}",
                "text": self.msgs
            },
            "at": {
                # "atMobiles": [
                #     "17707640806"
                # ], 
                "isAtAll": True
            }
        }

        tmpmsgs = self.msgs
        bak = requests.post(DingDingPush.dingdingpushURL,json=jsonReq )
        self.msgs = ''
        return bak, tmpmsgs

if __name__ == '__main__':
    DingDingPush.dingdingpushURL = 'https://oapi.dingtalk.com/robot/send?access_token=dce48b458945d20f3cb36ab05900287631bd5a39193b47879c8a5ed2e268d4b3'
    # dd = DingDingPush.pushMsg('asdf',True)
    # print(dd)
    dd = DingDingPush()
    dd.addmd('asd')
    p,o = dd.pushmd()
    print(p,o)