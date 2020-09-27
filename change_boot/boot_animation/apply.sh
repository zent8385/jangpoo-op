#! /bin/bash

cp -r ./splash.img /sdcard/splash.img
su
dd if=/sdcard/splash.img of=/dev/block/bootdevice/by-name/splash