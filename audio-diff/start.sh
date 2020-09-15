#!/bin/bash

input="diff.xlsx"  #样本数据格式是 ｜btId ｜url ｜数据类型｜
onurl="http://api-audio-bj.fengkongcloud.com/v2/saas/anti_fraud/audio"  #线上请求URL
opurl="http://api-audio-bj.fengkongcloud.com/v2/saas/anti_fraud/audio"  #私有化的URL

#请求线上
python3 audio_request.py $input $onurl #如果有线上数据，可以不打开


#请求私有化环境
python3 audio_request.py $input $output $opurl


#查询线上接口把结果保存到on_output文件中
on_output="result-online" #查询结果
on_query_url="http://api-audio-bj.fengkongcloud.com/v2/saas/anti_fraud/query_audio" #线上查询接口
python3 audio_query.py $on_output $on_query_url


#查询私有化接口把结果保存到oppo_output文件中
oppo_output="result-oppo"
oppo_query_url="http://api-audio-bj.fengkongcloud.com/v2/saas/anti_fraud/query_audio" #私有化查询接口
python3 audio_query.py $oppo_output $on_query_url


#根据oppo_output 和 on_output 做diff
python3 audio_diff.py $on_output $oppo_output 
