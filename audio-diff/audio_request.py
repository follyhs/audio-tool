import requests
import json
import time
import uuid
import pandas as pd
import sys
import getopt
import os

#accessKey ="J1VpmBnMKXvxNgg0eecJ"
accessKey ="X4nf23B7TpsQeKrGMD3G"
appId ="default"
audioType = "POLITICAL_ABUSE_PORN_AD_MOAN_ANTHEN"
callback = "http://127.0.0.1:19983"

def log(level, info):
    print("logLev=[{}]    info={}".format(level, info))

def xlsx2csv(inFile):
    data_xls = pd.read_excel(inFile, index_col=0)
    data_xls.to_csv("tmp.csv", encoding='utf-8')

#btId  |  url  |   type
def readData(path):
    xlsx2csv(path)
    with open("./tmp.csv", "r") as f:
        datas = f.readlines()
    return datas

def predict(argv):
    if len(argv) != 3:
        log("FATAL", "request argv len != 3")
        return
    path = argv[0]
    saasUrl  = argv[1]
    prefix = argv[2]
    datas = readData(path)
    datas = datas[1:]
    count = 0
    for line in datas:
        items = line.split(",")
        if len(items) != 3:
            log("ERROR", "items len !=3")
            continue

        count = count + 1
        if count % 10 == 0:
            print(count)
        headers = {
                'Content-Type': 'application/json'
            }
       
        realData = dict()
        data = dict()
        data["returnAllText"] = False
        data["url"] = items[1].strip()
        data["tokenId"] ="test2"
        realData["data"] = data
        realData["accessKey"] = accessKey       # o0vvgryiWbP988c8uV3K
        realData["appId"] = appId
        realData["type"] = audioType
        realData["btId"] = prefix + items[0]
        realData["contentType"] = "URL"
        realData["callback"] = callback
        try:
            result = json.loads(requests.post(saasUrl, data=json.dumps(realData), headers=headers).content.decode())
            log("INFO", result)
        except:
            log("ERROR", "request")
            continue
        time.sleep(1)

if __name__ == "__main__":
    predict(sys.argv[1:])
