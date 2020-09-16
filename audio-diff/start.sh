#!/bin/bash

input="re-audio-diff.xlsx"  #样本数据格式是 ｜btId ｜url ｜数据类型｜
opurl="http://test.fengkongcloud.com/v2/saas/anti_fraud/audio"  #私有化的URL

#请求私有化环境
python3 audio_request.py $input $output $opurl


#查询私有化接口把结果保存到oppo_output文件中
oppo_output="result-oppo"
oppo_query_url="http://test.fengkongcloud.com/v2/saas/anti_fraud/query_audio" #私有化查询接口
python3 audio_query.py $oppo_output $oppo_query_url

on_output="result-online"
#根据oppo_output 和 on_output 做diff
python3 audio_diff.py $on_output $oppo_output
