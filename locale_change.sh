#!/usr/bin/bash

# Android system locale
lang=ko-KR

# change system locale
setprop persist.sys.locale $lang
setprop persist.sys.local $lang
