#!/bin/bash
accesskey=X4nf23B7TpsQeKrGMD3G
org=xoSa2BLWub1q7xIzvvki
url=http://localhost:19091
callback=10.141.16.179

echo "-----start-----"
#robot -v accesskey:4Ky6AV4hE0pWLeG1bXNw -v url:http://10.141.56.227:80 -v callback-audio:http://10.141.16.179:8901/audio -v callback-queryData=http://10.141.16.179:8901/queryData -d results testcase/private-audio-oppo.txt

robot -v accesskey:$accesskey -v url:$url -v callback-audio:http://$callback:8901/audio -v callback-queryData=http://$callback:8901/queryData -d results testcase/private-audio-oppo.txt

