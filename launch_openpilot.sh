#!/usr/bin/bash

if [ ! -f "/data/no_ota_updates" ]; then
    /usr/bin/touch /data/no_ota_updates
fi

if [ -f "/data/openpilot/op.py" ]; then
    DIFF=$(/usr/bin/applets/diff /data/openpilot/op.py /system/comma/home/op.py)
    if [ "$DIFF" != "" ]; then
    sleep 3
    mount -o remount,rw /system
    cp -f /data/openpilot/op.sh /system/comma/home/
    cp -f /data/openpilot/op.py /system/comma/home/
    cp -f /data/openpilot/tune.sh /system/comma/home/
    chmod 755 /system/comma/home/op.sh
    chmod 644 /system/comma/home/op.py
    chmod 755 /system/comma/home/tune.sh
    mount -o remount,r /system
    fi
fi

if [ ! -f "/system/comma/home/op.py" ]; then
    sleep 3
    mount -o remount,rw /system
    cp -f /data/openpilot/op.sh /system/comma/home/
    cp -f /data/openpilot/op.py /system/comma/home/
    cp -f /data/openpilot/tune.sh /system/comma/home/
    chmod 755 /system/comma/home/op.sh
    chmod 644 /system/comma/home/op.py
    chmod 755 /system/comma/home/tune.sh
    mount -o remount,r /system
fi

ALIAS_CHECK1=$(/usr/bin/grep tu /system/comma/home/.bash_profile)
ALIAS_CHECK2=$(/usr/bin/grep op /system/comma/home/.bash_profile)

if [ "$ALIAS_CHECK1" == "" ]; then
    sleep 3
    mount -o remount,rw /system
    echo "alias tu='/system/comma/home/tune.sh'" >> /system/comma/home/.bash_profile
    mount -o remount,r /system
fi
if [ "$ALIAS_CHECK2" == "" ]; then
    sleep 3
    mount -o remount,rw /system
    echo "alias op='/system/comma/home/op.sh'" >> /system/comma/home/.bash_profile
    mount -o remount,r /system
fi

if [ ! -f "/system/fonts/opensans_regular.ttf" ]; then
    sleep 3
    mount -o remount,rw /system
  	cp -rf /data/openpilot/selfdrive/assets/fonts/opensans* /system/fonts/
    cp -rf /data/openpilot/kyd/fonts.xml /system/etc/fonts.xml
    chmod 644 /system/etc/fonts.xml
  	chmod 644 /system/fonts/opensans*
    mount -o remount,r /system
	
	setprop persist.sys.locale ko-KR
  	setprop persist.sys.local ko-KR
	setprop persist.sys.timezone Asia/Seoul
fi

export PASSIVE="0"
exec ./launch_chffrplus.sh

