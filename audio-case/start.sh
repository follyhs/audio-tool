#!/bin/bash
acskey="4Ky6AV4hE0pWLeG1bXNw"
org="RlokQwRlVjUrTUlkIqOg"
url=http://10.141.56.227:80
callback_ip=10.141.16.179

echo "##############执行audio-case"

robot -v accesskey:$acsskey -v url:$url -v callback-audio:http://$callback_ip:8901/video -v callback-queryData=http://$callback_ip:8901/queryData -d results "testcase/private-audio-oppo.txt"
