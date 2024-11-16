#!/bin/sh

DEVICE=$1
DEVICE_NAME=$(echo "${DEVICE//'/dev/'}")
LOG_FOLDER=/var/log/custom
LOG_FILE_PATH=$LOG_FOLDER/drive-health.log

# CREATE FOLDERS AND FILES IF NOT EXIST
if [ ! -f $LOG_FOLDER ]; then 
    mkdir -p $LOG_FOLDER
    chown -R 1000:1000 $LOG_FOLDER
fi

if [ ! -f $LOG_FILE_PATH ]; then 
    echo 'date,device_name,health_status' > $LOG_FILE_PATH    
    chown 1000:1000 $LOG_FILE_PATH
fi

# ROUTINE
OUTPUT=$(smartctl -H ${DEVICE} | grep 'SMART overall-health self-assessment test result: ')
RESULT=$(echo "${OUTPUT//'SMART overall-health self-assessment test result: '}")

echo $(date),$DEVICE_NAME,$RESULT >> $LOG_FILE_PATH
