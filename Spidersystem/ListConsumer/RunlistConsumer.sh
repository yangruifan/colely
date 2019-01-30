#!/bin/sh
pids=`ps -ef|grep "listConsumer.py"|grep -v "grep"|grep -v "$0"| awk '{print $2}'`
if [ "$pids" != "" ];then
    for  pid  in   $pids;
    do
        echo "kill pid: "$pid
        kill -9 $pid
    done
fi


cd /data/wwwroot/SpiderFrame/ListConsumer
nohup python3 -u  listConsumer.py >log.log 2>&1  &
