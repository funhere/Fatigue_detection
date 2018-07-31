#!/bin/bash
#
PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/bin

currday="`date +%Y-%m-%d`"
currsec="`date +%Y%m%d%H%M%S`"

#PS_COUNT=`ps aux | grep record_video | wc -l`
#if [ "$PS_COUNT" -gt 2 ]
#then
  #echo "Already recording! $PS_COUNT $currsec"
  #exit 1
#fi

disk_available=`df -h | grep /dev/root | awk '{print $5}'`
if [ {$disk_available:0:-1} -gt 90 ]
then
  echo "Not enough disk: $disk_available"
  exit 1
fi

mkdir -p /home/pi/Recordings/driving/$currday

raspivid -o - -t 0 -p 400,300,400,300 --framerate 24 --bitrate 17000000 --qp 20 --width 640 --height 360 | tee /home/pi/Recordings/driving/$currday/video-$currsec.h264 | cvlc stream:///dev/stdin --sout '#standard{access=http,mux=ts,dest=:8080' :demux=h264
