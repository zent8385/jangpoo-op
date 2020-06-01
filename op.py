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
print ("1. OP_BACKUP  - AUTO DIR BACKUP(branch_timestamp)")
print ("2. OP_RESTORE - AUTO RESTORE(LAST Bak DIR)")
print ("3. OP_BACKUP  - MANUAL BACKUP + kegman.json")
print ("4. OP_RESTORE - MANUAL RESTORE + kegman.json")
print ("5. OP_INSTALL - Install OP new. If exist OP directory, will be renamed")
print ("6. OP_UPDATE  - Run 'git pull' command to update OP latest")
print ("7. SEE_BRANCH - Confirm current branch")
print ("8. CH_BRANCH  - Branch change(pull latest, quick change and reboot")
print ("t. LIVE_TUNE  - Run live tune")
print ("r. REBOOT     - Reboot your EON")
print ("EXIT: anykey")
print ("")
print ("Please select job what you want")


char = getch()

if (char == "1"):
    os.system("clear")
    print ("Copying openpilot to openpilot_branch_timestamp...")
    os.system("cd /data; date +%Y%m%d%H%M%S > ctime.txt")
    os.system("cd /data/openpilot; branch=`git branch | grep '*' | awk -F' ' '{print $2}' | tail -n 1`; cd /data; ct=`cat ctime.txt`; cp -rfp /data/openpilot /data/openpilot_${branch}_${ct}")
    os.system("cd /data/openpilot; branch=`git branch | grep '*' | awk -F' ' '{print $2}' | tail -n 1`; cd /data; ct=`cat ctime.txt`; cp -f /data/kegman.json /data/kegman.json_${branch}_${ct}")
    os.system("rm -f /data/ctime.txt")
    print ("")
    print ("Your backup dir and kegman file are below")
    print ("")
    os.system("ls -drt /data/openpilot_* | tail -n 1")
    os.system("ls -tr /data/kegman* | tail -n 1")
    print ("")
    print ("Press p key to move first menu")

    char1 = getch()
    if (char1 == "p"):
        os.system("cd /system/comma/home; ./op.sh")

elif (char == "2"):
    os.system("clear")
    print ("Your last backup dir and kegman file are here")
    print ("")
    os.system("cd /data; ls -drt /data/openpilot_* | tail -n 1")
    os.system("ls -tr /data/kegman* | tail -n 1")
    print ("")
    print ("")
    print ("This will remove your openpilot directory")
    print ("and replace the op with current bak dir with kegman file")
    print ("If you don't see the backup dir Press n key")
    print ("Do yo want to continue?(y/n)")
    
    char2 = getch()

    if (char2 == "y"):
        os.system("cd /data; date +%Y%m%d%H%M%S > ctime.txt")
        os.system("cd /data/openpilot; git branch | grep '*' | awk -F' ' '{print $2}' | tail -n 1 > /data/branch.txt")
        os.system("cd /data; curopdir=`ls -aldrt /data/openpilot_* | awk -F '/' '{print $3}' | tail -n 1`; ; cd /data; ct=`cat ctime.txt`; branch=`cat branch.txt`; mv openpilot openpilot_temp_12345; mv $curopdir openpilot; mv openpilot_temp_12345 openpilot_${branch}_${ct}")
        os.system("cd /data; curkegman=`ls -altr /data/kegman.json_* | awk -F '/' '{print $3}' | tail -n 1`; cd /data; branch=`cat branch.txt`; ct=`cat ctime.txt`; mv kegman.json kegman.json_${branch}_${ct}; cp -f ${curkegman} kegman.json")
        os.system("rm -f /data/ctime.txt")
        os.system("rm -f /data/branch.txt")
        print ("")
        print ("Following is the result")
        os.system("cd /data; ls -aldrt /data/openpilot*")
        os.system("cd /data; ls -alrt /data/kegman.json*")
        print ("")
        print ("Do yo want to reboot?(y/n)")

        char21 = getch()

        if (char21 == "y"):
            os.system("reboot")
        elif (char21 == "n"):
            os.system("cd /system/comma/home; ./op.sh")

    elif (char2 == "n"):
        os.system("cd /system/comma/home; ./op.sh")


elif (char == "3"):
    os.system("clear")
    print ("Please type backup name you want to make")
    print ("")
    bakdir = input('BACKUP DIR NAME: openpilot_')
    os.system("clear")
    print ("Copying openpilot to openpilot_%s..." %bakdir)
    print ("Copying kegman.json to kegman.json_%s..." %bakdir)
    print ("")
    os.system("cp -rp /data/openpilot /data/openpilot_" + bakdir)
    os.system("cp -f /data/kegman.json /data/kegman.json_" + bakdir)
    print ("Your backup dir and kegman file are below")
    print ("")
    os.system("ls -drt /data/openpilot_" + bakdir + " | tail -n 1")
    os.system("ls -tr /data/kegman.json_" + bakdir + " | tail -n 1")
    print ("")
    print ("Press p key to move first menu")

    char3 = getch()
    if (char3 == "p"):
        os.system("cd /system/comma/home; ./op.sh")

elif (char == "4"):
    os.system("clear")
    print ("This will remove your openpilot directory")
    print ("And replace the openpilot with the dir you selected")
    print ("If the backup dir is not match or empty, Press n key")
    print ("")
    print ("Your BACKUP Directory is here")
    os.system("cd /data; ls -d openpilot_* | grep openpilot_")
    print ("")
    print ("and kegman.json file")
    os.system("cd /data; ls kegman.json_* | grep kegman.json_")
    print ("")
    print ("Next step, you can choose the bak dirs")
    print ("Press y key to continue,  p: move to first")

    char4 = getch()

    if (char4 == "y"):
        os.system("clear")
        print ("Please select the left side number you want to restore")
        print ("will be restored with matched kegman.json backup file")
        print ("If finished, will reboot automatically")
        print ("")
        os.system("cd /data; ls -d openpilot_* | grep -n openpilot_")

        char41 = getch()

        if (char41 == "1"):
            os.system("cd /data; ls -d openpilot_* | grep -n openpilot_ | grep 1: | awk -F ':' '{print $2}' | tail -n 1 > dir_temp.txt")
            fp = open('/data/dir_temp.txt', 'r')
            dir_data = fp.readline()
            fp.close()
            if (dir_data != ""):
                print ("")
                print ("On restoring your openpilot backup dir to openpilot...")
                os.system("rm -f /data/dir_temp.txt")
                os.system("cd /data; rm -rf openpilot; tdir=`ls -d openpilot_* | grep -n openpilot_ | grep 1: | awk -F ':' '{print $2}' | tail -n 1`; mv $tdir openpilot; cp -rfp openpilot $tdir")
                os.system("cd /data; tfile=`ls -d openpilot_* | grep -n openpilot_ | grep 1: | awk -F 'openpilot_' '{print $2}' | tail -n 1`; cp -f kegman.json_$tfile kegman.json")
                print ("Done. will reboot now...")
                os.system("reboot")
            else:
                os.system("rm -f /data/dir_temp.txt")
                print ("")
                print ("Aborted")
                print ("Your backup Directory is invalid")
        elif (char41 == "2"):
            os.system("cd /data; ls -d openpilot_* | grep -n openpilot_ | grep 2: | awk -F ':' '{print $2}' | tail -n 1 > dir_temp.txt")
            fp = open('/data/dir_temp.txt', 'r')
            dir_data = fp.readline()
            fp.close()
            if (dir_data != ""):
                print ("")
                print ("On copying your openpilot backup dir to openpilot...")
                os.system("rm -f /data/dir_temp.txt")
                os.system("cd /data; rm -rf openpilot; tdir=`ls -d openpilot_* | grep -n openpilot_ | grep 2: | awk -F ':' '{print $2}' | tail -n 1`; mv $tdir openpilot; cp -rfp openpilot $tdir")
                os.system("cd /data; tfile=`ls -d openpilot_* | grep -n openpilot_ | grep 2: | awk -F 'openpilot_' '{print $2}' | tail -n 1`; cp -f kegman.json_$tfile kegman.json")
                print ("Done. will reboot now...")
                os.system("reboot")
            else:
                os.system("rm -f /data/dir_temp.txt")
                print ("")
                print ("Aborted")
                print ("Your backup Directory is invalid")
        elif (char41 == "3"):
            os.system("cd /data; ls -d openpilot_* | grep -n openpilot_ | grep 3: | awk -F ':' '{print $2}' | tail -n 1 > dir_temp.txt")
            fp = open('/data/dir_temp.txt', 'r')
            dir_data = fp.readline()
            fp.close()
            if (dir_data != ""):
                print ("")
                print ("On copying your openpilot backup dir to openpilot...")
                os.system("rm -f /data/dir_temp.txt")
                os.system("cd /data; rm -rf openpilot; tdir=`ls -d openpilot_* | grep -n openpilot_ | grep 3: | awk -F ':' '{print $2}' | tail -n 1`; mv $tdir openpilot; cp -rfp openpilot $tdir")
                os.system("cd /data; tfile=`ls -d openpilot_* | grep -n openpilot_ | grep 3: | awk -F 'openpilot_' '{print $2}' | tail -n 1`; cp -f kegman.json_$tfile kegman.json")
                print ("Done. will reboot now...")
                os.system("reboot")
            else:
                os.system("rm -f /data/dir_temp.txt")
                print ("")
                print ("Aborted")
                print ("Your backup Directory is invalid")
                os.system("rm -f /data/dir_temp.txt")
        elif (char41 == "4"):
            os.system("cd /data; ls -d openpilot_* | grep -n openpilot_ | grep 4: | awk -F ':' '{print $2}' | tail -n 1 > dir_temp.txt")
            fp = open('/data/dir_temp.txt', 'r')
            dir_data = fp.readline()
            fp.close()
            if (dir_data != ""):
                print ("")
                print ("On copying your openpilot backup dir to openpilot...")
                os.system("rm -f /data/dir_temp.txt")
                os.system("cd /data; rm -rf openpilot; tdir=`ls -d openpilot_* | grep -n openpilot_ | grep 4: | awk -F ':' '{print $2}' | tail -n 1`; mv $tdir openpilot; cp -rfp openpilot $tdir")
                os.system("cd /data; tfile=`ls -d openpilot_* | grep -n openpilot_ | grep 4: | awk -F 'openpilot_' '{print $2}' | tail -n 1`; cp -f kegman.json_$tfile kegman.json")
                print ("Done. will reboot now...")
                os.system("reboot")
            else:
                os.system("rm -f /data/dir_temp.txt")
                print ("")
                print ("Aborted")
                print ("Your backup Directory is invalid")
        elif (char41 == "5"):
            os.system("cd /data; ls -d openpilot_* | grep -n openpilot_ | grep 5: | awk -F ':' '{print $2}' | tail -n 1 > dir_temp.txt")
            fp = open('/data/dir_temp.txt', 'r')
            dir_data = fp.readline()
            fp.close()
            if (dir_data != ""):
                print ("")
                print ("On copying your openpilot backup dir to openpilot...")
                os.system("rm -f /data/dir_temp.txt")
                os.system("cd /data; rm -rf openpilot; tdir=`ls -d openpilot_* | grep -n openpilot_ | grep 5: | awk -F ':' '{print $2}' | tail -n 1`; mv $tdir openpilot; cp -rfp openpilot $tdir")
                os.system("cd /data; tfile=`ls -d openpilot_* | grep -n openpilot_ | grep 5: | awk -F 'openpilot_' '{print $2}' | tail -n 1`; cp -f kegman.json_$tfile kegman.json")
                print ("Done. will reboot now...")
                os.system("reboot")
            else:
                os.system("rm -f /data/dir_temp.txt")
                print ("")
                print ("Aborted")
                print ("Your backup Directory is invalid")
        elif (char41 == "6"):
            os.system("cd /data; ls -d openpilot_* | grep -n openpilot_ | grep 6: | awk -F ':' '{print $2}' | tail -n 1 > dir_temp.txt")
            fp = open('/data/dir_temp.txt', 'r')
            dir_data = fp.readline()
            fp.close()
            if (dir_data != ""):
                print ("")
                print ("On copying your openpilot backup dir to openpilot...")
                os.system("rm -f /data/dir_temp.txt")
                os.system("cd /data; rm -rf openpilot; tdir=`ls -d openpilot_* | grep -n openpilot_ | grep 6: | awk -F ':' '{print $2}' | tail -n 1`; mv $tdir openpilot; cp -rfp openpilot $tdir")
                os.system("cd /data; tfile=`ls -d openpilot_* | grep -n openpilot_ | grep 6: | awk -F 'openpilot_' '{print $2}' | tail -n 1`; cp -f kegman.json_$tfile kegman.json")
                print ("Done. will reboot now...")
                os.system("reboot")
            else:
                os.system("rm -f /data/dir_temp.txt")
                print ("")
                print ("Aborted")
                print ("Your backup Directory is invalid")
        elif (char41 == "7"):
            os.system("cd /data; ls -d openpilot_* | grep -n openpilot_ | grep 7: | awk -F ':' '{print $2}' | tail -n 1 > dir_temp.txt")
            fp = open('/data/dir_temp.txt', 'r')
            dir_data = fp.readline()
            fp.close()
            if (dir_data != ""):
                print ("")
                print ("On copying your openpilot backup dir to openpilot...")
                os.system("rm -f /data/dir_temp.txt")
                os.system("cd /data; rm -rf openpilot; tdir=`ls -d openpilot_* | grep -n openpilot_ | grep 7: | awk -F ':' '{print $2}' | tail -n 1`; mv $tdir openpilot; cp -rfp openpilot $tdir")
                os.system("cd /data; tfile=`ls -d openpilot_* | grep -n openpilot_ | grep 7: | awk -F 'openpilot_' '{print $2}' | tail -n 1`; cp -f kegman.json_$tfile kegman.json")
                print ("Done. will reboot now...")
                os.system("reboot")
            else:
                os.system("rm -f /data/dir_temp.txt")
                print ("")
                print ("Aborted")
                print ("Your backup Directory is invalid")
        elif (char41 == "8"):
            os.system("cd /data; ls -d openpilot_* | grep -n openpilot_ | grep 8: | awk -F ':' '{print $2}' | tail -n 1 > dir_temp.txt")
            fp = open('/data/dir_temp.txt', 'r')
            dir_data = fp.readline()
            fp.close()
            if (dir_data != ""):
                print ("")
                print ("On copying your openpilot backup dir to openpilot...")
                os.system("rm -f /data/dir_temp.txt")
                os.system("cd /data; rm -rf openpilot; tdir=`ls -d openpilot_* | grep -n openpilot_ | grep 8: | awk -F ':' '{print $2}' | tail -n 1`; mv $tdir openpilot; cp -rfp openpilot $tdir")
                os.system("cd /data; tfile=`ls -d openpilot_* | grep -n openpilot_ | grep 8: | awk -F 'openpilot_' '{print $2}' | tail -n 1`; cp -f kegman.json_$tfile kegman.json")
                print ("Done. will reboot now...")
                os.system("reboot")
            else:
                os.system("rm -f /data/dir_temp.txt")
                print ("")
                print ("Aborted")
                print ("Your backup Directory is invalid")
        elif (char41 == "9"):
            os.system("cd /data; ls -d openpilot_* | grep -n openpilot_ | grep 9: | awk -F ':' '{print $2}' | tail -n 1 > dir_temp.txt")
            fp = open('/data/dir_temp.txt', 'r')
            dir_data = fp.readline()
            fp.close()
            if (dir_data != ""):
                print ("")
                print ("On copying your openpilot backup dir to openpilot...")
                os.system("rm -f /data/dir_temp.txt")
                os.system("cd /data; rm -rf openpilot; tdir=`ls -d openpilot_* | grep -n openpilot_ | grep 9: | awk -F ':' '{print $2}' | tail -n 1`; mv $tdir openpilot; cp -rfp openpilot $tdir")
                os.system("cd /data; tfile=`ls -d openpilot_* | grep -n openpilot_ | grep 9: | awk -F 'openpilot_' '{print $2}' | tail -n 1`; cp -f kegman.json_$tfile kegman.json")
                print ("Done. will reboot now...")
                os.system("reboot")
            else:
                os.system("rm -f /data/dir_temp.txt")
                print ("")
                print ("Aborted")
                print ("Your backup Directory is invalid")
    elif (char4 == "p"):
            os.system("cd /system/comma/home; ./op.sh")

elif (char == "5"):
    os.system("clear")
    print ("1. OPKR_0.7.3")
    print ("2. OPKR_0.7.4")
    print ("3. OPKR_0.7.5")
    print ("4. OPKR_0.7.3_BOLT")
    print ("5. OPKR_0.7.3_HKG_community")
    print ("6. OPKR_0.7.3_ATOM")
    print ("p. move to first menu")
    print ("EXIT: anykey")
    print ("")
    print ("Select Branch you want to install(number)")
    
    char5 = getch()

    if (char5 == "1"):    
        os.system("cd /data; date +%Y%m%d%H%M%S > ctime.txt")
        os.system("cd /data/openpilot; branch=`git branch | grep '*' | awk -F' ' '{print $2}' | tail -n 1`; cd /data; ct=`cat ctime.txt`; mv /data/openpilot /data/openpilot_${branch}_${ct}")
        os.system("rm -f /data/ctime.txt")
        os.system("cd /data; git clone https://github.com/openpilotkr/openpilot.git; cd openpilot; git checkout OPKR_0.7.3; reboot")
    elif (char5 == "2"):
        os.system("cd /data; date +%Y%m%d%H%M%S > ctime.txt")
        os.system("cd /data/openpilot; branch=`git branch | grep '*' | awk -F' ' '{print $2}' | tail -n 1`; cd /data; ct=`cat ctime.txt`; mv /data/openpilot /data/openpilot_${branch}_${ct}")
        os.system("rm -f /data/ctime.txt")
        os.system("cd /data; git clone https://github.com/openpilotkr/openpilot.git; cd openpilot; git checkout OPKR_0.7.4; reboot")
    elif (char5 == "3"):
        os.system("cd /data; date +%Y%m%d%H%M%S > ctime.txt")
        os.system("cd /data/openpilot; branch=`git branch | grep '*' | awk -F' ' '{print $2}' | tail -n 1`; cd /data; ct=`cat ctime.txt`; mv /data/openpilot /data/openpilot_${branch}_${ct}")
        os.system("rm -f /data/ctime.txt")
        os.system("cd /data; git clone https://github.com/openpilotkr/openpilot.git; cd openpilot; git checkout OPKR_0.7.5; reboot")
    elif (char5 == "4"):
        os.system("cd /data; date +%Y%m%d%H%M%S > ctime.txt")
        os.system("cd /data/openpilot; branch=`git branch | grep '*' | awk -F' ' '{print $2}' | tail -n 1`; cd /data; ct=`cat ctime.txt`; mv /data/openpilot /data/openpilot_${branch}_${ct}")
        os.system("rm -f /data/ctime.txt")
        os.system("cd /data; git clone https://github.com/openpilotkr/openpilot.git; cd openpilot; git checkout OPKR_0.7.3_BOLT; reboot")
    elif (char5 == "5"):
        os.system("cd /data; date +%Y%m%d%H%M%S > ctime.txt")
        os.system("cd /data/openpilot; branch=`git branch | grep '*' | awk -F' ' '{print $2}' | tail -n 1`; cd /data; ct=`cat ctime.txt`; mv /data/openpilot /data/openpilot_${branch}_${ct}")
        os.system("rm -f /data/ctime.txt")
        os.system("cd /data; git clone https://github.com/openpilotkr/openpilot.git; cd openpilot; git checkout OPKR_0.7.3_HKG_community; reboot")
    elif (char5 == "6"):
        os.system("cd /data; date +%Y%m%d%H%M%S > ctime.txt")
        os.system("cd /data/openpilot; branch=`git branch | grep '*' | awk -F' ' '{print $2}' | tail -n 1`; cd /data; ct=`cat ctime.txt`; mv /data/openpilot /data/openpilot_${branch}_${ct}")
        os.system("rm -f /data/ctime.txt")
        os.system("cd /data; git clone https://github.com/openpilotkr/openpilot.git; cd openpilot; git checkout OPKR_0.7.3_ATOM; reboot")
    elif (char5 == "p"):
        os.system("cd /system/comma/home; ./op.sh")

elif (char == "6"):
    print ("")
    os.system("cd /data/openpilot; git pull")
    print ("")
    print ("Press p key to move first menu")

    char6 = getch()

    if (char6 == "p"):
        os.system("cd /system/comma/home; ./op.sh")

elif (char == "7"):
    print ("")
    print ("Your current branch is")
    os.system("cd /data/openpilot; git branch")
    print ("")
    print ("Press p key to move first menu")

    char7 = getch()

    if (char7 == "p"):
        os.system("cd /system/comma/home; ./op.sh")

elif (char == "8"):
    os.system("clear")
    print ("1. OPKR_0.7.3")
    print ("2. OPKR_0.7.4")
    print ("3. OPKR_0.7.5")
    print ("4. OPKR_0.7.3_BOLT")
    print ("5. OPKR_0.7.3_HKG_community")
    print ("6. OPKR_0.7.3_ATOM")
    print ("p. move to first menu")
    print ("EXIT: anykey")
    print ("")
    print ("Select Branch you want to change(number)")
    print ("Changing the branch and reboot will occur automatically")

    char8 = getch()

    if (char8 == "1"):
        os.system("cd /data/openpilot; git pull")
        os.system("cd /data/openpilot; git checkout OPKR_0.7.3")
        os.system("cd /data/openpilot; git pull")
        os.system("reboot")
    elif (char8 == "2"):
        os.system("cd /data/openpilot; git pull")
        os.system("cd /data/openpilot; git checkout OPKR_0.7.4")
        os.system("cd /data/openpilot; git pull")
        os.system("reboot")
    elif (char8 == "3"):
        os.system("cd /data/openpilot; git pull")
        os.system("cd /data/openpilot; git checkout OPKR_0.7.5")
        os.system("cd /data/openpilot; git pull")
        os.system("reboot")
    elif (char8 == "4"):
        os.system("cd /data/openpilot; git pull")
        os.system("cd /data/openpilot; git checkout OPKR_0.7.3_BOLT")
        os.system("cd /data/openpilot; git pull")
        os.system("reboot")
    elif (char8 == "5"):
        os.system("cd /data/openpilot; git pull")
        os.system("cd /data/openpilot; git checkout OPKR_0.7.3_HKG_community")
        os.system("cd /data/openpilot; git pull")
        os.system("reboot")
    elif (char8 == "6"):
        os.system("cd /data/openpilot; git pull")
        os.system("cd /data/openpilot; git checkout OPKR_0.7.3_ATOM")
        os.system("cd /data/openpilot; git pull")
        os.system("reboot")
    elif (char8 == "p"):
        os.system("cd /system/comma/home; ./op.sh")

elif (char == "t"):
    os.system("cd /data/openpilot; ./tune.sh")

elif (char == "r"):
    os.system("reboot")