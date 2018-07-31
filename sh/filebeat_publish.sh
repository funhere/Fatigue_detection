#!/bin/sh

echo "$PWD/filebeat/dt_filebeat.yml"

filebeat -e -c "$PWD/filebeat/dt_filebeat.yml" -d "publish"
