#!/bin/bash

opurl="http://10.0.20.53:19091/v2/saas/anti_fraud/audio"  #私有化的URL
#opurl="http://api-audio-bj.fengkongcloud.com/v2/saas/anti_fraud/audio"  #私有化的URL
qps=50
count=50000

python audio_request.py $qps $opurl $count #如果有线上数据，可以不打开
