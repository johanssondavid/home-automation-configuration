import appdaemon.plugins.hass.hassapi as hass
import datetime
import appdaemon
import time

SAMPLE_TIME = 60
SECONDS_BETWEEN_RUN = 60 * 60 * 42
SECONDS_ACTIVE_CONSIDER_CLEAN = 60*30

class Xiaomi(hass.Hass):
  def initialize(self):
    self.log("initialize xiaomi app")

    self.run_in(self.callback, SAMPLE_TIME)

    #self.listen_state(self.someone_came_home_cb, "group.all_devices", old = "not_home", new = "home")

    self.next_run = SECONDS_BETWEEN_RUN
    self.time_until_consider_cleaned = SECONDS_ACTIVE_CONSIDER_CLEAN

  #def someone_came_home_cb(self):
  #    if self.get_state(entity_id="vacuum.xiaomi_vacuum_cleaner") == "on":
  #      self.call_service("vacuum.turn_off")

  def dnd_active(self):
    dndStart = datetime.datetime.strptime(self.entities.vacuum.xiaomi_vacuum_cleaner.attributes.do_not_disturb_start, '%H:%M:%S')
    dndEnd = datetime.datetime.strptime(self.entities.vacuum.xiaomi_vacuum_cleaner.attributes.do_not_disturb_end, '%H:%M:%S')

    now = datetime.datetime.now()

    early = now.time() < dndEnd.time()
    late = now.time() > dndStart.time()
    dnd_boolean = self.get_state(entity_id="input_boolean.vacuum_automation") == "off" or self.get_state(entity_id="automations_off") == "on"
    someone_is_home = self.get_state(entity_id="group.all_devices") == "home"

    return early or late or dnd_boolean or someone_is_home

  def callback(self, debug):
    isRobotOn = self.get_state(entity_id="vacuum.xiaomi_vacuum_cleaner") == "on"

    if isRobotOn:
      if self.time_until_consider_cleaned <= 0:
        self.next_run = SECONDS_BETWEEN_RUN
      else:
        self.time_until_consider_cleaned -= SAMPLE_TIME
    else:
      self.time_until_consider_cleaned = SECONDS_ACTIVE_CONSIDER_CLEAN
      self.next_run -= SAMPLE_TIME

    if self.next_run <= 0:
      if not(self.dnd_active()):
        self.turn_on("vacuum.xiaomi_vacuum_cleaner")
        self.notify("Starting vacuum")

    self.log("Robot %s, next %ds, until clean %ds" % (str(isRobotOn), self.next_run, self.time_until_consider_cleaned))
    self.run_in(self.callback, SAMPLE_TIME)
