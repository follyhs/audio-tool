import requests
import json
import time
import uuid
import pandas as pd
import sys
import getopt
import os
import random


url="https://audio-annotation-1251671073.cos.ap-shanghai.myqcloud.com/05ba0f62fe13f4acde073dd22beb3431_a0004.wav"
accessKey ="4Ky6AV4hE0pWLeG1bXNw"
appId="default"
audioType = "POLITICAL_ABUSE_PORN_AD_MOAN_ANTHEN"
callback="http://127.0.0.1:19983"

def log(level, info):
    print("logLev=[{}]    info={}".format(level, info))

def predict(argv):
    if len(argv) != 3:
        log("ERROR", "argv len != 3")
        return
    qps = int(argv[0])
    saasUrl  = argv[1]
    reqCount = int(argv[2])
    if qps < 1:
        qps = 1
    wait = 1 / qps
    
    for i in range(reqCount):
        headers = {
                'Content-Type': 'application/json'
            }
        realData = dict()
        data = dict()
        data["returnAllText"] = False
        data["url"] = url
        data["tokenId"] ="test2"
        realData["data"] = data
        realData["accessKey"] = accessKey       # o0vvgryiWbP988c8uV3K
        realData["appId"] = appId
        realData["type"] = audioType
        realData["btId"] = "tool-" + str(random.randint(0,100000))
        realData["contentType"] = "URL"
        realData["callback"] = callback
        print(json.dumps(realData)) 
        
        try:
            result = json.loads(requests.post(saasUrl, data=json.dumps(realData), headers=headers).content.decode())
            log("INFO", result)
        except:
            log("ERROR", "request")
            continue
        time.sleep(wait)

if __name__ == "__main__":
    predict(sys.argv[1:])
