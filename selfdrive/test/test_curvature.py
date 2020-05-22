# flake8: noqa
import math
import numpy as np
import os
from common.apk import update_apks, start_frame, pm_apply_packages, android_packages
from common.params import Params
from common.testing import phone_only
from selfdrive.manager import manager_init, manager_prepare
from selfdrive.manager import start_managed_process, kill_managed_process, get_running
from selfdrive.manager import start_daemon_process
from selfdrive.car.hyundai.spdcontroller  import SpdController
from functools import wraps
from selfdrive.config import Conversions as CV
import common.MoveAvg as  moveavg1
import cereal.messaging as messaging

import json
import requests
import signal
import subprocess
import time


movAvg = moveavg1.MoveAvg()   


MAX_SPEED = 255


sc = SpdController()
path_x = np.arange(192)




def main():

    sm=None 
    if sm is None:
        sm = messaging.SubMaster(['plan', 'pathPlan', 'model'])

        v_ego = 50 * CV.KPH_TO_MS
        print('curvature test ')
        while True:
          sm.update(0)
          value, model_sum = sc.calc_va( sm, v_ego )
          print( 'curvature={:.3f} sum={:.5f}'.format( value, model_sum ) )
          




if __name__ == "__main__":
  main()
  # manual exit because we are forked
  #sys.exit(0)
