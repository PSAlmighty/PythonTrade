#!/bin/sh
pids=`ps ax | grep -v grep | grep -E 'Xvfb|chromium|chromedriver' | awk '{print $1}'`
[ -z "$pids" ] || kill -9 $pids
