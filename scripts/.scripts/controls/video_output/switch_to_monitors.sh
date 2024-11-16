#!/bin/bash

nvidia-settings --assign CurrentMetaMode="DP-0: 2560x1440_144 +5120+0 {AllowGSYNCCompatible=On}, DP-4: 2560x1440_144 +2560+0 {AllowGSYNCCompatible=On}, USB-C-0: 2560x1440_144 +0+0 {AllowGSYNCCompatible=On}"
sleep 1

#python3 /home/sandro/.config/scripts/python/switch_sound.py -d speakers
#sleep 1
