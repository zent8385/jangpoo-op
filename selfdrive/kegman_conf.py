import json
import os

class kegman_conf():
  def __init__(self, CP=None):
    self.conf = self.read_config()
    if CP is not None:
      self.init_config(CP)

  def init_config(self, CP):
    write_conf = False
    if self.conf['tuneGernby'] != "1":
      self.conf['tuneGernby'] = str(1)
      write_conf = True
	
    # only fetch Kp, Ki, Kf sR and sRC from interface.py if it's a PID controlled car
    if CP.lateralTuning.which() == 'pid':
      if self.conf['Kp'] == "-1":
        self.conf['Kp'] = str(round(CP.lateralTuning.pid.kpV[0],3))
        write_conf = True
      if self.conf['Ki'] == "-1":
        self.conf['Ki'] = str(round(CP.lateralTuning.pid.kiV[0],3))
        write_conf = True
      if self.conf['Kf'] == "-1":
        self.conf['Kf'] = str('{:f}'.format(CP.lateralTuning.pid.kf))
        write_conf = True
    
    if self.conf['steerRatio'] == "-1":
      self.conf['steerRatio'] = str(round(CP.steerRatio,3))
      write_conf = True
    
    if self.conf['steerRateCost'] == "-1":
      self.conf['steerRateCost'] = str(round(CP.steerRateCost,3))
      write_conf = True

    if write_conf:
      self.write_config(self.config)

  def read_config(self):
    self.element_updated = False

    if os.path.isfile('/data/kegman.json'):
      with open('/data/kegman.json', 'r') as f:
        self.config = json.load(f)

      if "cameraOffset" not in self.config:
        self.config.update({"cameraOffset":"0.06"})
        self.element_updated = True

      if "battPercOff" not in self.config:
        self.config.update({"battPercOff":"30"})
        self.config.update({"carVoltageMinEonShutdown":"11800"})
        self.config.update({"brakeStoppingTarget":"0.25"})
        self.element_updated = True

      if "tuneGernby" not in self.config:
        self.config.update({"tuneGernby":"1"})
        self.config.update({"Kp":"-1"})
        self.config.update({"Ki":"-1"})
        self.element_updated = True

      if "liveParams" not in self.config:
        self.config.update({"liveParams":"1"})
        self.element_updated = True
	
      if "steerRatio" not in self.config:
        self.config.update({"steerRatio":"-1"})
        self.config.update({"steerRateCost":"-1"})
        self.element_updated = True
	
      if "leadDistance" not in self.config:
        self.config.update({"leadDistance":"5"})
        self.element_updated = True
	
      if "deadzone" not in self.config:
        self.config.update({"deadzone":"10.0"})
        self.element_updated = True
	
      if "1barBP0" not in self.config:
        self.config.update({"1barBP0":"-0.1"})
        self.config.update({"1barBP1":"2.25"})
        self.config.update({"2barBP0":"-0.1"})
        self.config.update({"2barBP1":"2.5"})
        self.config.update({"3barBP0":"0.0"})
        self.config.update({"3barBP1":"3.0"})
        self.element_updated = True


      if "1barMax" not in self.config:
        self.config.update({"1barMax":"2.1"})
        self.config.update({"2barMax":"2.1"})
        self.config.update({"3barMax":"2.1"})
        self.element_updated = True
	
      if "1barHwy" not in self.config:
        self.config.update({"1barHwy":"0.4"})
        self.config.update({"2barHwy":"0.3"})
        self.config.update({"3barHwy":"0.1"})
        self.element_updated = True
	
      if "slowOnCurves" not in self.config:
        self.config.update({"slowOnCurves":"1"})
        self.element_updated = True
	
      if "Kf" not in self.config:
        self.config.update({"Kf":"-1"})
        self.element_updated = True
	
      if "sR_boost" not in self.config:
        self.config.update({"sR_boost":"0"})
        self.config.update({"sR_BP0":"0"})
        self.config.update({"sR_BP1":"0"})
        self.config.update({"sR_time":"0.2"})
        self.element_updated = True

      if "ALCnudgeLess" not in self.config:
        self.config.update({"ALCnudgeLess":"0"})
        self.config.update({"ALCminSpeed":"16.666667"})
        self.element_updated = True

      if "ALCtimer" not in self.config:
        self.config.update({"ALCtimer":"1.0"})
        self.element_updated = True

      if "CruiseDelta" not in self.config:
        self.config.update({"CruiseDelta":"8"})
        self.element_updated = True

      if "CruiseEnableMin" not in self.config:
        self.config.update({"CruiseEnableMin":"0"})
        self.element_updated = True

      if "epsModded" not in self.config:
        self.config.update({"epsModded":"0"})
        self.element_updated = True
      
      if "steerTorqueOver" not in self.config:
        self.config.update({"steerTorqueOver":"360"})
        self.element_updated = True

      if "threshold" not in self.config:
        self.config.update({"threshold":"150"})
        self.element_updated = True

      if "cV_Ratio" not in self.config:
        self.config.update({"cV_Ratio":"0.7"})
        self.element_updated = True

      if "cV_Dist" not in self.config:
        self.config.update({"cV_Dist":"-5"})
        self.element_updated = True
      
      
      if "cruise_set_mode" not in self.config:
        self.config.update({"cruise_set_mode":"0"})
        self.element_updated = True
      
      if "deltaUp" not in self.config:
        self.config.update({"deltaUp":"3"})
        self.element_updated = True

      if "deltaDown" not in self.config:
        self.config.update({"deltaDown":"5"})
        self.element_updated = True
        
      if "steerMax" not in self.config:
        self.config.update({"steerMax":"409"})
        self.element_updated = True


      if self.element_updated:
        print("updated")
        self.write_config(self.config)

    else:
      self.config = {"cameraOffset":"0.06", "lastTrMode":"1", "battChargeMin":"70", "battChargeMax":"80", \
                     "wheelTouchSeconds":"30000", "battPercOff":"30", "carVoltageMinEonShutdown":"11800", \
                     "brakeStoppingTarget":"0.25", "tuneGernby":"1", \
                     "Kp":"-1", "Ki":"-1", "liveParams":"1", "leadDistance":"5", "deadzone":"10.0", \
                     "1barBP0":"-0.1", "1barBP1":"2.25", "2barBP0":"-0.1", "2barBP1":"2.5", "3barBP0":"0.0", \
                     "3barBP1":"3.0", "1barMax":"2.1", "2barMax":"2.1", "3barMax":"2.1", \
                     "1barHwy":"0.4", "2barHwy":"0.3", "3barHwy":"0.1", \
                     "steerRatio":"-1", "steerRateCost":"-1", "slowOnCurves":"1", "Kf":"-1", \
                     "sR_boost":"0", "sR_BP0":"0", "sR_BP1":"0", "sR_time":"0.2", \
                     "ALCnudgeLess":"0", "ALCminSpeed":"16.666667", "ALCtimer":"1.0", "CruiseDelta":"8", \
                     "CruiseEnableMin":"0", "epsModded": "0", "steerTorqueOver":"360", "threshold":"150", \
                     "cv_Ratio":"0.7", "cv_Dist":"-5", "cruise_set_mode": "0", "deltaUp": "3", "deltaDown": "5", "steerMax":"409"}




      self.write_config(self.config)
    return self.config

  def write_config(self, config):
    try:
      with open('/data/kegman.json', 'w') as f:
        json.dump(self.config, f, indent=2, sort_keys=True)
        os.chmod("/data/kegman.json", 0o764)
    except IOError:
      os.mkdir('/data')
      with open('/data/kegman.json', 'w') as f:
        json.dump(self.config, f, indent=2, sort_keys=True)
        os.chmod("/data/kegman.json", 0o764)
