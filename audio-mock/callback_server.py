# -*- coding:utf-8 -*-
from flask import Flask
from flask import request
import pymysql
import json
import socket
import re


app = Flask(__name__)


# video_data = {"checksum":"1765accd4d815372d12147c48797ff69a440a4461c97bed5812999b4b53ec490","result":"{\"code\":1100,\"message\":\"\\u6210\\u529f\",\"requestId\":\"c949e0de22ecbf8e61f4b31f46313af0\",\"btId\":\"1585118118083816\",\"riskLevel\":\"PASS\",\"callbackParam\":{\"url\":\"12345678\"}}"}


mysqlip = "10.66.191.34"
mysqluser = "root"
mysqlpassword = "shumeitest2018"
database_name = "saas"

#判断表是否在库中
def table_exists(con, table_name):
    sql = "show tables;"
    con.execute(sql)
    tables = [con.fetchall()]
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    if table_name in table_list:
        # 存在返回1
        return 1
    else:
        # 不存在返回0
        return 0

#创建数据库
def create_database(table_name):
    # db = MySQLdb.connect(mysqlip, mysqluser, mysqlpassword, "saas", charset='utf8')
    db = pymysql.connect(
        host=mysqlip,
        user=mysqluser,
        passwd=mysqlpassword
    )
    cur = db.cursor()
    # sql = 'create database if not exists {}'.format(database_name)
    # cur.execute(sql)
    cur.execute("use {}".format(database_name))
    # if (table_exists(cur, table_name) == 1):
    #     pass
    # else:
    #     sql = 'create table {}(' \
    #           '`id` bigint(11) NOT NULL AUTO_INCREMENT,' \
    #           '`requestId` varchar(40) NOT NULL,' \
    #           '`callback_data` longblob,' \
    #           '`insert_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,' \
    #           'PRIMARY KEY (`id`)' \
    #           ') ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COMMENT='视频类回调结果收集表')'.format(table_name)
    #     cur.execute(sql)
    #     db.commit()

    try:
        print ("create table start!")
        sql = 'create table if not exists {}(`id` bigint(11) NOT NULL AUTO_INCREMENT,`requestId` varchar(40) NOT NULL,`callback_data` longblob,`insert_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,PRIMARY KEY (`id`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4;'.format(table_name)
        cur.execute(sql)
        db.commit()
        db.close()
        print ("Create table success")
    except:
        print ("Create table failed")
        return False


# 插入回调结果
def DbAction(sql, *args):

    # db = MySQLdb.connect(mysqlip, mysqluser, mysqlpassword, database_name, charset='utf8')
    db = pymysql.connect(
        host=mysqlip,
        user=mysqluser,
        passwd=mysqlpassword
    )
    cursor = db.cursor()
    # print(args)
    try:
        cursor.execute(sql, args)
        db.commit()
        print("commit")
    except:
        db.rollback()
        print("rollback")
    db.close()

# 查询回调结果
def queryDb(sql, *args):
    # db = MySQLdb.connect(mysqlip, mysqluser, mysqlpassword, database_name, charset='utf8')
    db = pymysql.connect(
        host=mysqlip,
        user=mysqluser,
        passwd=mysqlpassword
    )
    cursor = db.cursor()
    # print(args)
    result = ""
    try:
        cursor.execute(sql, args)
        result = cursor.fetchone()[0]
        print("successful")
    except:
        print("error")
    db.close()
    return result

# 获取回调服务脚本所在ip
def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    print("本机host:",ip)
    return ip


@app.route('/audio',methods=["GET","POST"])
def audio():
    res = {"code":200,"msg":"audio"}
    callback_data = json.loads(request.get_data())
    requestId = callback_data["requestId"]
    print(callback_data["requestId"])
    # print callback_data

    insert_callback_data = str(json.dumps(callback_data))
    # 使用转义的方法
    # insert_callback_data = str(json.dumps(callback_data)).replace("\\", "\\\\")
    # sql = "insert into audio_callback (requestId,callback_data) values ('%s','%s');"%(requestId,insert_callback_data)

    sql = "insert into audio_callback (requestId,callback_data) values (%s,%s);"
    # print(sql)
    # sql_data = [requestId, insert_callback_data]
    DbAction(sql, requestId, insert_callback_data)
    return str(res)

@app.route('/video',methods=["GET","POST"])
def video():
    res = {"code":200,"msg":"video"}
    video_json = json.loads(request.get_data())
    result = video_json["result"]
    # print result
    requestId = json.loads(result)["requestId"]
    print (requestId)
    # video结果插入数据库
    insert_callback_data = str(json.dumps(video_json))
    print(insert_callback_data)
    sql = "insert into video_callback (requestId,callback_data) values (%s,%s);"
    # print(sql)
    # sql_data = [requestId, insert_callback_data]
    DbAction(sql, requestId, insert_callback_data)

    return str(res)

@app.route('/queryData',methods=["GET","POST"])
def queryData():
    print(request.get_data())
    response = json.loads(request.get_data())
    event = response["event"]
    reqid = response["requestId"]
    # print(event,reqid)
    if event == "audio":
        sql = "select callback_data from audio_callback where requestId = %s;"
        audiodata = queryDb(sql, reqid)
        # print(audiodata)
        res = str(audiodata)
        return res
    elif event == "video":
        sql = "select callback_data from video_callback where requestId = %s;"
        videodata = queryDb(sql, reqid)
        print(videodata)
        res = str(videodata)
        return res
    else:
        res = {"code":200,"msg":"查询失败"}
        return str(res)




if __name__ == '__main__':
    create_database("video_callback")
    create_database("audio_callback")
    localhost = get_host_ip()
    app.run(host=localhost, port=8901, debug=True)
    # video(video_data)

