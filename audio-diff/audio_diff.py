import requests
import json
import time
import uuid
import pandas as pd
import sys
import getopt
import os
import json
import demjson

def log(level, info):
    print("logLev=[{}]    info={}".format(level, info))

def xlsx2csv(inFile):
    data_xls = pd.read_excel(inFile, index_col=0)
    data_xls.to_csv("tmp.csv", encoding='utf-8')

#btId  |  result
def readData(inFile):
    with open(inFile, "r") as f:
        datas = f.read()
    return datas

def diffProc(oppo, online):
    opRes = json.loads(oppo)
    onRes = json.loads(online)
    if opRes["riskLevel"] == onRes["riskLevel"] and opRes["labels"] == onRes["labels"]:
        return False
    return True

def writeFile(online, oppo):
    res = dict()
    res["online"] = {"riskLevel":online["riskLevel"], "labels":online["labels"]}
    res["oppo"] = {"riskLevel":online["riskLevel"], "labels":online["labels"]}
    with open("diff-result", "a") as f:
        f.write(json.dumps(res) + "\n")

def predict(argv):
    log("DEBUG", argv)
    if len(argv) != 2:
        log("ERROR", "diff argv len != 2")
        return
    online = argv[0]
    oppo   = argv[1]
    
    onData = json.loads(readData(online))
    opData = json.loads(readData(oppo))

    if len(onData) != len(opData):
        log("ERROR", "len(oppo) != len(online)")
    count = 0
    result = {}
    for key, value in onData.items():
        res = opData.get(key)
        if res != None and diffProc(res, value):
            count += 1
            writeFile(value, res)
    print("result:", count/len(onData))
    os.remove(oppo)
if __name__ == "__main__":
    predict(sys.argv[1:])
