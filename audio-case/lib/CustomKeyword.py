#!usr/bin/env python
#encoding=utf-8
'''this file is creat for diy keyword'''

import json
import os
import base64
import binascii
import hashlib
import sys
import collections
import xlrd
import uuid
import jsonpointer
import jsonpatch


from xlutils.copy import copy
from data_constant import *

sys.path.append('..')
reload(sys)
sys.setdefaultencoding('utf-8')

# 计算图片的base64(base64中包含\n)
def Base64FunStr(filepath):
    f=open(filepath,'rb')
    #imgBase64=base64.b64encode(f.read())
    imgBase64=base64.encodestring(f.read())
    f.close()
    return imgBase64

# 计算图片的base64(base64中不包含\n)
def Base64Fun(filepath):
    f=open(filepath,'rb')
    imgBase64=base64.b64encode(f.read())
    #imgBase64=base64.encodestring(f.read())
    f.close()
    return imgBase64


def sjsonToDict(DictStr):
    try:
        return json.loads(DictStr)
    except:
        return 'this string not a dictionary string'

# 字符串或字典转为json
def ContentToJson(content):
    try:
        if isinstance(content,str):
            data = json.loads(content)
            data = json.JSONEncoder().encode(data)
            return data
        if isinstance(content,dict):
            data = json.JSONEncoder().encode(content)
            return data
    except:
        return content

def JsonDecode(content):
    try:
        data = json.loads(content)
        value = data.keys()
        #print value
        str= '{'
        for key in value:
            if data[key]:
                mdict = '"'+key+'":"'+data[key]+'",',
            else:
                mdict = '"'+key+'":"null"',
        sjson = str + mdict + '}'
        return sjson
    except:
        return content

def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return data.encode('utf-8')
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data


def oderdict_transfer(testdict):
    orderdict = collections.OrderedDict()
    for key in sorted(testdict.keys()):
        value = testdict[key]
        if isinstance(value, dict):
            orderdict[key] = oderdict_transfer(value)
        elif isinstance(value, list):
            for i in range(len(value)):
                if isinstance(value[i], dict):
                    value[i] = oderdict_transfer(value[i])
            orderdict[key] = sorted(value)
            for j in value:
                if not (isinstance(j, dict)):
                    orderdict[key] = value
                    break
        else:
            orderdict[key] =value
    return orderdict

def sort_json_keys(content):
    try:
        if isinstance(content,str):
            data = json.loads(content)
            data = json.dumps(data,sort_keys=True)
            return data
        if isinstance(content,dict):
            data = json.dumps(content,sort_keys=True)
            return data
    except:
        return content

def json_key_sort(jsontext):
    '''
       json transfer order by key:

       Example:
       |${json_dump} |json_key_sort | ${json_text}|
       '''
    json_dict=json_loads_byteified(jsontext)
    print(json_dict.pop('requestId'))
    orderdict_result = oderdict_transfer(json_dict)
    if 'imgs' in orderdict_result.keys():
        orderdict_result['imgs'] = sorted(orderdict_result['imgs'],key=lambda dicttemp: dicttemp['btId'])
    print(orderdict_result)
    json_dump =json.dumps(orderdict_result)
    return json_dump


def write_file(filename,writecontent):
    with open(filename, 'a') as f:
        f.write(writecontent + '\n')

def delete_file(filename):
    if os.path.exists(filename):
        os.remove(filename)

def generate_btId():
    reuuid = uuid.uuid1()
    btId = str(reuuid)
    print btId
    return btId.translate(None,'-')

class CustomKeyword(object):
    def open_excelfile(self, excelfilepath):
        self.excelfilepath = excelfilepath
        self.data_table = xlrd.open_workbook(excelfilepath).sheets()[0]
        self.btId = ""
        print self.excelfilepath

    def get_title_line(self):
        '''
           get excel case titile list:

           Example:
           |${titlelist} |get_title_line| ${filepath}|
           '''
        titlelist = self.data_table.col_values(excel_data_column["title"])
        titlelist.pop(0)
        return titlelist

    def get_switch_status(self,lineindex):
        swich_status = self.data_table.cell(lineindex + 1,excel_data_column["switch_status"]).value
        return swich_status

    def generate_input_data(self,lineindex):
        '''
           generate request data;

           Example:
           |${reqdata} |generate_input_data | %{lineindex} | ${filepath}|
           '''
        input_line = self.data_table.row_values(lineindex + 1)
        reqdata_dict = {
            "data":{
            }
        }
        for element in audio_reqdata_excel_list:
            ctype = self.data_table.cell(lineindex + 1, excel_data_column[element]).ctype  # 判断数据类型
            # print element
            element_list = element.split("-")
            # print(element_list)
            input_element = input_line[excel_data_column[element]]
            if input_element == "NonExist":
                continue
            elif element == "callbackParam":
                reqdata_dict[element] = json.loads(input_element)
                print(input_element)
                continue
            elif element_list[0] == "data":
                # print ctype
                if ctype == 4:
                    reqdata_dict["data"][element_list[1]] = True if self.data_table.cell(lineindex+1,
                                excel_data_column[element]) == 1 else False  # 处理布尔型
                elif ctype == 2 and input_element % 1 == 0:
                # 判断数据为数值，改为整型
                    reqdata_dict["data"][element_list[1]] = int(input_element)
                # elif element_list[1] == "timestamp" or element_list[1] == "level":
                #     reqdata_dict["data"][element_list[1]] = int(input_element)
                    print reqdata_dict["data"][element_list[1]]
                elif element_list[1] == "content":
                    reqdata_dict["data"][element_list[1]] = Base64Fun(input_element)
                    continue
                elif element_list[1] == "formatInfo":
                    reqdata_dict["data"][element_list[1]] = json.loads(input_element)
                    continue
                else:
                    reqdata_dict["data"][element_list[1]] = input_element
                continue
            else:
                reqdata_dict[element] = input_element
        if input_line[excel_data_column["btId"]] == "YES":
            self.btId = generate_btId()
            reqdata_dict["btId"] = self.btId
        print (reqdata_dict)
        reqdata = ContentToJson(reqdata_dict)
        # print(reqdata)
        return reqdata

    def generate_query_data(self,lineindex):
        '''
           generate request data;

           Example:
           |${reqdata} |generate_input_data | %{lineindex} | ${filepath}|
           '''
        input_line = self.data_table.row_values(lineindex + 1)
        queryvideo_data_dict = {}
        for element in audio_query_list:
            input_element = input_line[excel_data_column[element]]
            if input_element == "NonExist":
                continue
            else:
                queryvideo_data_dict[element] = input_line[excel_data_column[element]]
        if input_line[excel_data_column["btId"]] == "YES":
            queryvideo_data_dict["btId"] = self.btId
        print(queryvideo_data_dict)
        reqdata = ContentToJson(queryvideo_data_dict)
        return reqdata

    def get_v4_input_data(self,lineindex):
        '''
           generate request data;
           Example:
           |${reqdata} |generate_input_data | %{lineindex} | ${filepath}|
        '''
        input_line = self.data_table.row_values(lineindex + 1)
        # print(input_line)
        reqdata = input_line[excel_data_column["reqdata"]]
        # print(input_line[video_data_column["btid_isunicq"]])
        # for element in audio_reqdata_excel_list:

        reqdata = json.loads(reqdata)
        if input_line[excel_data_column["btid_isunicq"]] == "YES":
            self.btId = generate_btId()
            # print self.btId
            reqdata["btId"] = self.btId

        if input_line[excel_data_column["content_isbase64"]] =="YES":
            reqdata["content"] = Base64Fun(input_line[excel_data_column["audio_file"]])
            # print req_json_data
        # else:
        req_json_data = ContentToJson(reqdata)
        # print req_json_data
        return req_json_data

    def write_into_excel(self,lineindex,content, *writedatalist):
        '''
           write things which you want to record into excel;

           Example:
           |write_into_excel | %{lineindex} | ${filepath}| ${content}| *writedatalist
           '''
        data = xlrd.open_workbook(self.excelfilepath)
        copy_data = copy(data)
        for writedata in writedatalist:
            copy_data.get_sheet(0).write(lineindex + 1, excel_data_column[writedata], content)
        copy_data.save(self.excelfilepath)

    def get_expected_input(self, lineindex):
        input_line = self.data_table.row_values(lineindex + 1)
        expected_data = input_line[excel_data_column["expect_output"]]
        return expected_data

    def get_element_input(self, lineindex,element):
        input_line = self.data_table.row_values(lineindex + 1)
        expected_data = input_line[excel_data_column[element]]
        return expected_data

    def get_json_value(self,json_string, json_pointer):
        """
        Get the target node of the JSON document `json_string` specified by `json_pointer`.
        Example:
        | ${result}=       | Get Json Value   | {"foo": {"bar": [1,2,3]}} | /foo/bar |
        | Should Be Equal  | ${result}        | [1, 2, 3]                 |          |
        """
        value = json.dumps(jsonpointer.resolve_pointer(json_string, json_pointer)).decode('utf-8')
        return value.decode('unicode-escape')

    def readfile(file):
        with open(file, 'r') as f:
            data = f.read()
            str = ''.join(data)
            return str


