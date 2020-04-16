#!/usr/bin/bash

if [ ! -f /data/ota_updates ]; then
    /usr/bin/touch /data/no_ota_updates
fi

setprop persist.sys.locale $lang
setprop persist.sys.local $lang

export PASSIVE="0"
exec ./launch_chffrplus.sh

