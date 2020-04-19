import math
import numpy as np

from selfdrive.controls.lib.speed_smoother import speed_smoother
from selfdrive.config import Conversions as CV
from selfdrive.car.hyundai.values import Buttons, SteerLimitParams, LaneChangeParms
from common.numpy_fast import clip, interp

import common.log as trace1

MAX_SPEED = 255.0

LON_MPC_STEP = 0.2  # first step is 0.2s
MAX_SPEED_ERROR = 2.0
AWARENESS_DECEL = -0.2     # car smoothly decel at .2m/s^2 when user is distracted

# lookup tables VS speed to determine min and max accels in cruise
# make sure these accelerations are smaller than mpc limits
_A_CRUISE_MIN_V  = [-1.0, -.8, -.67, -.5, -.30]
_A_CRUISE_MIN_BP = [   0., 5.,  10., 20.,  40.]

# need fast accel at very low speed for stop and go
# make sure these accelerations are smaller than mpc limits
_A_CRUISE_MAX_V = [1.2, 1.2, 0.65, .4]
_A_CRUISE_MAX_V_FOLLOWING = [1.6, 1.6, 0.65, .4]
_A_CRUISE_MAX_BP = [0.,  6.4, 22.5, 40.]

# Lookup table for turns
_A_TOTAL_MAX_V = [1.7, 3.2]
_A_TOTAL_MAX_BP = [20., 40.]

# 75th percentile
SPEED_PERCENTILE_IDX = 7


def calc_cruise_accel_limits(v_ego, following):
  a_cruise_min = interp(v_ego, _A_CRUISE_MIN_BP, _A_CRUISE_MIN_V)

  if following:
    a_cruise_max = interp(v_ego, _A_CRUISE_MAX_BP, _A_CRUISE_MAX_V_FOLLOWING)
  else:
    a_cruise_max = interp(v_ego, _A_CRUISE_MAX_BP, _A_CRUISE_MAX_V)
  return np.vstack([a_cruise_min, a_cruise_max])



def limit_accel_in_turns(v_ego, angle_steers, a_target, CP):
  """
  This function returns a limited long acceleration allowed, depending on the existing lateral acceleration
  this should avoid accelerating when losing the target in turns
  """

  a_total_max = interp(v_ego, _A_TOTAL_MAX_BP, _A_TOTAL_MAX_V)
  a_y = v_ego**2 * angle_steers * CV.DEG_TO_RAD / (CP.steerRatio * CP.wheelbase)
  a_x_allowed = math.sqrt(max(a_total_max**2 - a_y**2, 0.))

  return [a_target[0], min(a_target[1], a_x_allowed)]


class SpdController():
  def __init__(self):
    self.long_control_state = 0  # initialized to off
    self.long_active_timer = 0
    self.long_wait_timer = 0

    self.v_acc_start = 0.0
    self.a_acc_start = 0.0
    self.path_x = np.arange(192)


    self.traceSC = trace1.Loger("SPD_CTRL")


  def reset(self):
    self.long_active_timer = 0


  def update(self, v_ego_kph, CS, sm, actuators ):
    btn_type = Buttons.NONE
    #lead_1 = sm['radarState'].leadOne
    v_ego = CS.v_ego

    if len(sm['model'].path.poly):
      path = list(sm['model'].path.poly)

      # Curvature of polynomial https://en.wikipedia.org/wiki/Curvature#Curvature_of_the_graph_of_a_function
      # y = a x^3 + b x^2 + c x + d, y' = 3 a x^2 + 2 b x + c, y'' = 6 a x + 2 b
      # k = y'' / (1 + y'^2)^1.5
      # TODO: compute max speed without using a list of points and without numpy
      y_p = 3 * path[0] * self.path_x**2 + 2 * path[1] * self.path_x + path[2]
      y_pp = 6 * path[0] * self.path_x + 2 * path[1]
      curv = y_pp / (1. + y_p**2)**1.5

      a_y_max = 2.975 - v_ego * 0.0375  # ~1.85 @ 75mph, ~2.6 @ 25mph
      v_curvature = np.sqrt(a_y_max / np.clip(np.abs(curv), 1e-4, None))
      model_speed = np.min(v_curvature)
      model_speed = max(20.0 * CV.MPH_TO_MS, model_speed) # Don't slow down below 20mph

      model_speed = model_speed * CV.MS_TO_KPH
      if model_speed > MAX_SPEED:
          model_speed = MAX_SPEED
    else:
      model_speed = MAX_SPEED

    #following = lead_1.status and lead_1.dRel < 45.0 and lead_1.vLeadK > v_ego and lead_1.aLeadK > 0.0

    following = CS.lead_distance < 70.0
    accel_limits = [float(x) for x in calc_cruise_accel_limits(v_ego, following)]
    jerk_limits = [min(-0.1, accel_limits[0]), max(0.1, accel_limits[1])]  # TODO: make a separate lookup for jerk tuning
    accel_limits_turns = limit_accel_in_turns(v_ego, CS.angle_steers, accel_limits, self.CP)

    # if required so, force a smooth deceleration
    accel_limits_turns[1] = min(accel_limits_turns[1], AWARENESS_DECEL)
    accel_limits_turns[0] = min(accel_limits_turns[0], accel_limits_turns[1])


    self.v_cruise, self.a_cruise = speed_smoother(self.v_acc_start, self.a_acc_start,
                                                  CS.cruise_set_speed,
                                                  accel_limits_turns[1], accel_limits_turns[0],
                                                  jerk_limits[1], jerk_limits[0],
                                                  LON_MPC_STEP)

    self.v_model, self.a_model = speed_smoother(self.v_acc_start, self.a_acc_start,
                                                  model_speed,
                                                  2*accel_limits[1], accel_limits[0],
                                                  2*jerk_limits[1], jerk_limits[0],
                                                  LON_MPC_STEP)


    v_delta = 0
    if CS.pcm_acc_status and CS.AVM_Popup_Msg == 1:
      v_delta = CS.VSetDis - CS.clu_Vanz

      if CS.lead_distance < 90:
        if self.long_active_timer == 0 and v_delta <= -2:
          pass
        else:
          self.long_active_timer += 1
          if self.long_active_timer < 10:
              self.long_wait_timer = 0
              btn_type = Buttons.SET_DECEL   # Vuttons.RES_ACCEL
          else:
              self.long_wait_timer += 1
              if self.long_wait_timer > 10:
                self.long_active_timer = 0
      else:
        self.long_active_timer = 0
        self.long_wait_timer = 0

    else:
      self.long_active_timer = 0

    # CS.driverOverride   # 1 Acc,  2 bracking, 0 Normal

    str1 = 'VD={:.1f}  dis={:.1f} VSet={:.0f} ss={:.1f}'.format( v_delta, CS.lead_distance, CS.VSetDis, CS.cruise_set_speed_kph )
    str2 = 'btn={:.0f} btn_type={}'.format(  CS.AVM_View, btn_type )
    #str3 = 'max{:.1f} d{} v{} a{} v{} a{}'.format( model_speed, lead_1.dRel, lead_1.vLeadK, lead_1.aLeadK, self.v_model, self.a_model )
    str3 = 'max{:.1f}  m=v{:.1f} a{:.1f}  c=v{:.1f} a{:.1f}'.format( model_speed, self.v_model, self.a_model, self.v_cruise, self.a_cruise )


    self.traceSC.add( 'v_ego={:.1f}  {} {} {}'.format( v_ego_kph, str1, str2, str3 )  )
    trace1.printf2( '{} {}'.format( str1, str3) )
    return btn_type, CS.clu_Vanz