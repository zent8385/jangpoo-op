#!/usr/bin/bash

/usr/bin/sh /data/openpilot/kyd/fonts/installer.sh &
export PASSIVE="0"
exec ./launch_chffrplus.sh

