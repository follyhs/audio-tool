#!/bin/bash
set -e

mysqlip="10.66.191.34"
mysqluser="root"
mysqlpassword="shumeitest2018"
filename=callback_server.py

sed -i "16c\mysqlip = \"${mysqlip}\"" ${filename}
sed -i "17c\mysqluser = \"${mysqluser}\"" ${filename}
sed -i "18c\mysqlpassword = \"${mysqlpassword}\"" ${filename}

nohup python ${filename} >callback.log 2>&1 &

exit 0

