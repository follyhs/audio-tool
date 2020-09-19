#!/usr/bin/python
# -*- coding: utf-8 -*-
# @File    : generate_reqdata.py
import time
from random import randint
from itertools import combinations
# from faker import Faker
import faker
fake = faker.Faker()
# print  fake.name()

def timestamp():
    t = int(round(time.time()*1000))
    return t

def combinations_reqdatalist(list):
    pool = tuple(list)
    r = len(pool)
    print r
    for p in range(r):
        print(p)
        for i in combinations(pool,p):
            print i
            # return i

def generateData(*args, **kwds):
    pools = map(list, args) * kwds.get('repeat', 1)
    generatedate = [[]]
    for pool in pools:
        generatedate = [x + [y] for x in generatedate for y in pool]
    return generatedate

# def audioreqdata(generatedate, txt):
#     # 打开txt文件，设定写入模式
#
#     out = open(txt, 'w')
#     title = '用例名称' + '\t' + '执行开关' + '\t' + '输入数据' + '\t' + '预期输出' + '\n'
#     out.write(title)
#     for g in generatedate:
#         accessKey = g[0]
#         type = g[1]
#         appId = g[2]
#         btid = g[3]
#         callback = g[4]
#         audioName = g[5]
#         ip = g[6]
#         channel = g[7]
#         returnAllText = g[8]
#         tokenId = g[9]
#         url = g[10]
#         # 用例名称
#         casename = str(accessKey) + '_' + str(type) + '_' + str(appId) + '_' + str(btid) + '_' + str(callback)\
#                    + '_' + str(audioName) + '_' + str(ip) + '_' + str(channel) + '_' + str(returnAllText) + '_' + \
#                    str(tokenId) + '_' + str(url) + '\t'
#         # 执行开关
#         status = 'yes' + '\t'
#
#         # req数据拼接
#         reqdata = '{"accessKey": "%s", "type": "%s", "appId": "%s", "btid": "%s", "callback": "%s",' \
#                   '"data": {"audioName": "%s", "ip": "%s", "channel": "%s", "returnAllText": %s, ' \
#                   '"tokenId": "%s","url": "%s"}, "callbackParam":{"test1": 1, "test2": "test-2", ' \
#                   '"test3": True}}'% (accessKey,type,appId,btid,callback,audioName,ip,channel,returnAllText,
#                     tokenId,url)+ '\t' + '\n'
#         print "reqdata: %s" + reqdata
#         out.write(casename)
#         out.write(status)
#         out.write(reqdata)




if __name__ == "__main__":
    accessKey = ['S4AUW8LLJIdomF6uFYHP', fake.name(), fake.date(pattern="%Y-%m-%d"), 'null', '\u6cd5\u8f6e\u529f',
                 'false', 'true']
    type = ['DEFAULT',]
    appId = ['default']
    btid = [timestamp()]
    callback = ['http://10.141.39.56:8000/']
    audioName = [fake.name()]
    ip = [fake.ipv4(network=False)]
    channel = ['audio']
    returnAllText = [True, False, None]
    tokenId = [timestamp()]
    url = ['http://sdkalarm.cdn.bcebos.com/20181201_150703.m4a','http://12345.mp3']
    callbackParam = {"test1":1 , "test2":"test-2","test3": True }
    reqList = ['accessKey','type','appId','btid','callback','audioName','ip','channel','returnAllText','tokenId','url']
    combinations_reqdatalist(reqList)


