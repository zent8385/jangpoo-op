import subprocess
import os
import time
from datetime import datetime

BASEDIR = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../"))

import sys, termios, tty, os, time

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

os.system("clear")
print ("1. OPBACKUP   - OP backup as openpilot_timestamp with kegman.json file")
print ("2. OPINSTALL  - install OP new. if exist OP directory, will be renamed")
print ("3. OPUPDATE   - run 'git pull' command to update OP latest")
print ("4. OPRESTORE  - replace OP with last OP backup directory")
print ("5. SEEBRANCH  - confirm current branch")
print ("6. CHBRANCH   - branch change(pull latest, quick change and reboot")
print ("EXIT: anykey")
print ("")
print ("Please select job what you want(number)")


char = getch()

if (char == "1"):
    os.system("clear")
    ct = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
    print ("Copying openpilot to openpilot_(timestamp)...")
    os.system("cp -rp /data/openpilot /data/openpilot_" + ct)
    os.system("cp -f /data/kegman.json /data/kegman.json_" + ct)
    os.system("ls -altr /data")
    print ("")
    print ("Your backup dir is above")
    print ("Press r key to move first menu")

    char1 = getch()
    if (char1 == "r"):
        os.system("cd /system/comma/home; ./op.sh")


elif (char == "2"):
    os.system("clear")
    print ("1. OPKR_0.7.3")
    print ("2. OPKR_0.7.4")
    print ("3. OPKR_0.7.5")
    print ("4. OPKR_0.7.3_BOLT")
    print ("5. OPKR_0.7.3_HKG_community")
    print ("6. OPKR_0.7.3_ATOM")
    print ("r. move to first menu")
    print ("EXIT: anykey")
    print ("")
    print ("Select Branch you want to install(number)")
    
    char2 = getch()

    if (char2 == "1"):    
        ct = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        os.system("mv /data/openpilot /data/openpilot_0.7.3_" + ct)
        os.system("cd /data; git clone https://github.com/openpilotkr/openpilot.git; cd openpilot; git checkout OPKR_0.7.3; reboot")
    elif (char2 == "2"):
        ct = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        os.system("mv /data/openpilot /data/openpilot_0.7.4_" + ct)
        os.system("cd /data; git clone https://github.com/openpilotkr/openpilot.git; cd openpilot; git checkout OPKR_0.7.4; reboot")
    elif (char2 == "3"):
        ct = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        os.system("mv /data/openpilot /data/openpilot_0.7.5_" + ct)
        os.system("cd /data; git clone https://github.com/openpilotkr/openpilot.git; cd openpilot; git checkout OPKR_0.7.5; reboot")
    elif (char2 == "4"):
        ct = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        os.system("mv /data/openpilot /data/openpilot_0.7.3_bolt_" + ct)
        os.system("cd /data; git clone https://github.com/openpilotkr/openpilot.git; cd openpilot; git checkout OPKR_0.7.3_BOLT; reboot")
    elif (char2 == "5"):
        ct = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        os.system("mv /data/openpilot /data/openpilot_0.7.3_HKG_community_" + ct)
        os.system("cd /data; git clone https://github.com/openpilotkr/openpilot.git; cd openpilot; git checkout OPKR_0.7.3_HKG_community; reboot")
    elif (char2 == "6"):
        ct = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        os.system("mv /data/openpilot /data/openpilot_0.7.3_ATOM_" + ct)
        os.system("cd /data; git clone https://github.com/openpilotkr/openpilot.git; cd openpilot; git checkout OPKR_0.7.3_ATOM; reboot")
    elif (char2 == "r"):
        os.system("cd /system/comma/home; ./op.sh")

elif (char == "3"):
    print ("")
    os.system("cd /data/openpilot; git pull")
    print ("")
    print ("Press r key to move first menu")

    char3 = getch()

    if (char3 == "r"):
        os.system("cd /system/comma/home; ./op.sh")

elif (char == "4"):
    os.system("clear")
    print ("Your last backup dir is here. check if it is")
    print ("")
    os.system("cd /data; ls -aldrt /data/openpilot_*")
    print ("")
    print ("")
    print ("This will remove your openpilot directory")
    print ("And replace the openpilot dir with current bak dir")
    print ("If you don't see the backup dir Press n key")
    print ("Do yo want to continue?(y/n)")
    
    char4 = getch()

    if (char4 == "y"):
        os.system("cd /data; rm -rf openpilot; curopdir=`ls -aldrt /data/openpilot_* | awk -F '/' '{print $3}' | tail -n 1`; mv $curopdir openpilot")
        print ("Following is the result")
        os.system("cd /data; ls -aldrt /data/openpilot*")
        print ("")
        print ("Do yo want to reboot?(y/n)")

        char41 = getch()

        if (char41 == "y"):
            os.system("reboot")
        elif (char41 == "n"):
            os.system("cd /system/comma/home; ./op.sh")

    elif (char4 == "n"):
        os.system("cd /system/comma/home; ./op.sh")



elif (char == "5"):
    print ("")
    print ("Your current branch is")
    os.system("cd /data/openpilot; git branch")
    print ("")
    print ("Press r key to move first menu")

    char5 = getch()

    if (char5 == "r"):
        os.system("cd /system/comma/home; ./op.sh")

elif (char == "6"):
    os.system("clear")
    print ("1. OPKR_0.7.3")
    print ("2. OPKR_0.7.4")
    print ("3. OPKR_0.7.5")
    print ("4. OPKR_0.7.3_BOLT")
    print ("5. OPKR_0.7.3_HKG_community")
    print ("6. OPKR_0.7.3_ATOM")
    print ("r. move to first menu")
    print ("EXIT: anykey")
    print ("")
    print ("Select Branch you want to change(number)")
    print ("Changing the branch and reboot will occur automatically")

    char6 = getch()

    if (char6 == "1"):
        os.system("cd /data/openpilot; git pull")
        os.system("cd /data/openpilot; git checkout OPKR_0.7.3")
        os.system("cd /data/openpilot; git pull")
        os.system("reboot")
    elif (char6 == "2"):
        os.system("cd /data/openpilot; git pull")
        os.system("cd /data/openpilot; git checkout OPKR_0.7.4")
        os.system("cd /data/openpilot; git pull")
        os.system("reboot")
    elif (char6 == "3"):
        os.system("cd /data/openpilot; git pull")
        os.system("cd /data/openpilot; git checkout OPKR_0.7.5")
        os.system("cd /data/openpilot; git pull")
        os.system("reboot")
    elif (char6 == "4"):
        os.system("cd /data/openpilot; git pull")
        os.system("cd /data/openpilot; git checkout OPKR_0.7.3_BOLT")
        os.system("cd /data/openpilot; git pull")
        os.system("reboot")
    elif (char6 == "5"):
        os.system("cd /data/openpilot; git pull")
        os.system("cd /data/openpilot; git checkout OPKR_0.7.3_HKG_community")
        os.system("cd /data/openpilot; git pull")
        os.system("reboot")
    elif (char6 == "6"):
        os.system("cd /data/openpilot; git pull")
        os.system("cd /data/openpilot; git checkout OPKR_0.7.3_ATOM")
        os.system("cd /data/openpilot; git pull")
        os.system("reboot")
    elif (char6 == "r"):
        os.system("cd /system/comma/home; ./op.sh")