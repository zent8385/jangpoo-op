#!/usr/bin/bash

if [ ! -f /data/ota_updates ]; then
    /usr/bin/touch /data/no_ota_updates
fi

if [ ! -f "/data/font_updated" ]; then
    update_font=1
else
	update_font=0
fi

if [ $update_font -eq "1" ]; then
    # sleep 3 secs in case, make sure the /system is re-mountable
    sleep 3
    mount -o remount,rw /system
		# install font
        cp -rf /data/openpilot/selfdrive/assets/fonts/opensans* /system/fonts/
        # change permissions
        chmod 644 /system/etc/fonts.xml
        chmod 644 /system/fonts/opensans*

    mount -o remount,r /system

/usr/bin/touch /data/font_updated

fi

# change system locale
setprop persist.sys.locale ko-KR
setprop persist.sys.local ko-KR

export PASSIVE="0"
exec ./launch_chffrplus.sh

