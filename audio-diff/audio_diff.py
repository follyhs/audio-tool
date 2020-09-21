import requests
import json
import time
import uuid
import pandas as pd
import sys
import getopt
import os
import json

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
    if opRes.get("riskLevel") == None or onRes.get("riskLevel") == None or opRes.get("labels") == None or onRes.get("labels") == None:
      return False

    if opRes["riskLevel"] == onRes["riskLevel"] and opRes["labels"] == onRes["labels"]:
        return False
    return True

def writeFile(online, oppo):
    onlinej = json.loads(online)
    oppoj = json.loads(oppo)
    res = dict()
    tmp = dict() 
    tmp["riskLevel"] = onlinej["riskLevel"]
    tmp["labels"] = onlinej["labels"]
    tmp["requestId"] = onlinej["requestId"] 
    res["online"] = tmp
    tmp2 = dict()
    tmp2["riskLevel"] = oppoj["riskLevel"]
    tmp2["labels"] = oppoj["labels"]
    tmp2["requestId"] = oppoj["requestId"] 
    res["oppo"] = tmp2
    with open("diff-result", "a") as f:
        f.write(json.dumps(res) + "\n")

def predict(argv):
    #log("DEBUG", argv)
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
    print("result: ", "different: ",count, "total: ", len(onData))
if __name__ == "__main__":
    predict(sys.argv[1:])
