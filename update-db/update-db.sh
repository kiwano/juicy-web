#!/bin/bash

updatedir=/home/kris/web/juicy/update-db
logdir=$updatedir/logs

$updatedir/rss-feeds.py >> $logdir/rss-feeds.log
$updatedir/weather.py >> $logdir/weather.log
