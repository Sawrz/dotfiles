#!/bin/sh
SLEEP_TIME=10

/home/sandro/.scripts/controls/drives/health_check_drive.sh /dev/sda
sleep ${SLEEP_TIME}s

/home/sandro/.scripts/controls/drives/health_check_drive.sh /dev/sdb
sleep ${SLEEP_TIME}s

/home/sandro/.scripts/controls/drives/health_check_drive.sh /dev/sdc
sleep ${SLEEP_TIME}s

/home/sandro/.scripts/controls/drives/health_check_drive.sh /dev/sdd
sleep ${SLEEP_TIME}s

/home/sandro/.scripts/controls/drives/health_check_drive.sh /dev/sde
sleep ${SLEEP_TIME}s

/home/sandro/.scripts/controls/drives/health_check_drive.sh /dev/sdf
sleep ${SLEEP_TIME}s

/home/sandro/.scripts/controls/drives/health_check_drive.sh /dev/sdg
sleep ${SLEEP_TIME}s

/home/sandro/.scripts/controls/drives/health_check_drive.sh /dev/sdh
sleep ${SLEEP_TIME}s

/home/sandro/.scripts/controls/drives/health_check_drive.sh /dev/sdi
sleep ${SLEEP_TIME}s

/home/sandro/.scripts/controls/drives/health_check_drive.sh /dev/sdj
sleep ${SLEEP_TIME}s
