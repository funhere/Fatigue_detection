#!/bin/bash

LOG_FILE=/home/pi/Works/video/log.txt

echo "Process: " >> "$LOG_FILE"
ps aux | grep record_video >> "$LOG_FILE" 2>&1
echo "" >> "$LOG_FILE"

echo "Files: " >> "$LOG_FILE"
find /media/pi/306f002f-cacc-4cfa-b4e9-021b3d2b3259/rpivideo/ -type f -exec ls -lh {} \; >> "$LOG_FILE" 2>&1
echo "" >> "$LOG_FILE"

echo "Recent cron logs: " >> "$LOG_FILE"
tail -20 /var/log/syslog | grep CRON >> "$LOG_FILE" 2>&1
echo "" >> "$LOG_FILE"
