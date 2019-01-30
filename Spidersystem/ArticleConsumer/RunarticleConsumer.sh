#!/bin/sh
pids=`ps -ef|grep "articleConsumer.py"|grep -v "grep"|grep -v "$0"| awk '{print $2}'`
if [ "$pids" != "" ];then
    for  pid  in   $pids;
    do
        echo "kill pid: "$pid
        kill -9 $pid
    done
fi


cd /data/wwwroot/SpiderFrame/ArticleConsumer
nohup python3 -u  articleConsumer.py >log.log 2>&1  &
