# -*- coding:utf-8 -*-
__author__ = 'yangx'

excel_data_column = {
    "title": 0,
    "switch_status":1,
    "accessKey":2,
    "type":3,
    "appId":4,
    "btId":5,
    "callback":6,
    "callbackParam":7,
    "data-url":8,
    "data-returnAllText":9,
    "data-audioName":10,
    "data-channel":11,
    "data-tokenId":12,
    "data-nickname":13,
    "data-timestamp":14,
    "data-ip":15,
    "data-phone":16,
    "data-deviceId":17,
    "data-receiveTokenId":18,
    "data-level":19,
    "data-role":20,
    "data-room":21,
    "data-imei":22,
    "data-mac":23,
    "data-idfv":24,
    "data-idfa":25,
    "data-content":26,
    "data-formatInfo":27,
    "audio_expect_output":28,
    "audio_actual_output":29,
    "query_switch": 30,
    "query_wait_time":31,
    "queryaudio_expect_output": 32,
    "queryaudio_actual_output": 33,
    "log_switch": 35,
    "log_data": 36,
    "btid_isunicq": 2,
    "content_isbase64":3,
    "audio_file":4,
    "reqdata": 5,
    "expect_code": 6,
    "actual_code": 7,
    "actual_output": 8,
    "case_id": 9
}

data_column = {
    "title": 0,
    "switch_status": 1,
    "input":2,
    "expect_output":3,
    "actual_output":4,
    "case_comment": 5
}

# audio_data = {
#     "accessKey":"${accesskey}",
#     "type":"PORN",
#     "appId":"default",
#     "btid":"${btid}",
#     "callback":"http://10.141.39.56:8000/",
#     "callbackParam":{
#         "testcallbackParam":"test"
#     },
#     "data":{
#         "url":"http://static-1253442168.file.myqcloud.com/lecture_advance_audio/7062850_1529054831000.mp3",
#         "audioName":"可选值",
#         "ip":"10.0.23.32可选",
#         "channel":"AUDIO",
#         "tokenId":"toekn123",
#         "returnAllText":True
#     }
# }

audio_query_list = ["accessKey","btId"]
audio_reqdata_excel_list = ["accessKey","type","appId","btId","callback","callbackParam","data-url",
                          "data-returnAllText","data-audioName","data-channel","data-tokenId","data-nickname",
                          "data-timestamp","data-ip","data-phone","data-deviceId","data-receiveTokenId",
                          "data-level","data-role","data-room","data-imei","data-mac","data-idfv","data-idfa",
                          "data-content","data-formatInfo"]
#excelfilepath = "../data/img_datadriven.xls"