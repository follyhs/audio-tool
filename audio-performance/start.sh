#!/bin/bash

opurl="http://118.89.221.77/v2/saas/anti_fraud/audio"  #私有化的URL
#opurl="http://api-audio-bj.fengkongcloud.com/v2/saas/anti_fraud/audio"  #私有化的URL
qps=10
count=10

python audio_request.py $qps $opurl $count #如果有线上数据，可以不打开
