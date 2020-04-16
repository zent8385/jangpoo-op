#!/usr/bin/bash

if [ ! -f /data/ota_updates ]; then
    /usr/bin/touch /data/no_ota_updates
fi

if [ ! -f "/data/locale_updated" ]; then
    update_locale=1
else
	update_locale=0
fi

if [ $update_locale -eq "1" ]; then
	setprop persist.sys.locale ko-KR
	setprop persist.sys.local ko-KR

/usr/bin/touch /data/locale_updated
fi

export PASSIVE="0"
exec ./launch_chffrplus.sh

