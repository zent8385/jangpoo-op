
from selfdrive.car.hyundai.values import Buttons, SteerLimitParams, LaneChangeParms, CAR
from common.numpy_fast import clip, interp

import common.log as trace1


class SpdController():
  def __init__(self):
    self.long_control_state = 0  # initialized to off
    self.long_active_timer = 0

  def reset(self):
    self.long_active_timer = 0


  def update(self, v_ego_kph, CS, actuators):
    btn_type = Buttons.NONE

    if CS.pcm_acc_status and CS.AVM_Popup_Msg == 1:
      self.long_active_timer += 1
      if self.long_active_timer < 10:
        btn_type = Buttons.SET_DECEL   # Vuttons.RES_ACCEL
    else:
      self.long_active_timer = 0

    # CS.driverOverride   # 1 Acc,  2 bracking, 0 Normal

    str1 = 'dis={:.1f} VSet={:.1f} Vanz={:.1f}  cmd={:.0f}'.format( CS.lead_distance, CS.VSetDis, CS.clu_Vanz, acc_mode )
    str2 = 'acc{} btn={:.0f}'.format(  CS.pcm_acc_status, CS.AVM_Popup_Msg )
    
    trace1.printf2( '{} {}'.format( str1, str2) )
    return btn_type, CS.clu_Vanz