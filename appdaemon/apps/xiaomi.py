import appdaemon.plugins.hass.hassapi as hass
import datetime
import appdaemon
import time

SAMPLE_TIME = 60
SECONDS_BETWEEN_RUN = 60 * 60 * 18
SECONDS_ACTIVE_CONSIDER_CLEAN = 60*30

class Xiaomi(hass.Hass):
  def initialize(self):
    self.log("initialize xiaomi app")

    self.run_in(self.callback, SAMPLE_TIME)

    self.next_run = SECONDS_BETWEEN_RUN
    self.time_until_consider_cleaned = SECONDS_ACTIVE_CONSIDER_CLEAN

  def dnd_active(self):
    dndStart = datetime.datetime.strptime(self.entities.vacuum.xiaomi_vacuum_cleaner.attributes.do_not_disturb_start, '%H:%M:%S')
    dndEnd = datetime.datetime.strptime(self.entities.vacuum.xiaomi_vacuum_cleaner.attributes.do_not_disturb_end, '%H:%M:%S')

    now = datetime.datetime.now()

    early = now.time() < dndEnd.time()
    late = now.time() > dndStart.time()
    dnd_boolean = self.get_state("input_boolean.vacuum_automation") == "off" or self.get_state("automations_off") == "on"
    someone_is_home = self.get_state("group.all_devices") == "home"

    return early or late or dnd_boolean or someone_is_home

  def callback(self, debug):
    isRobotOn = self.get_state("vacuum.xiaomi_vacuum_cleaner") == "on"

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
          self.call_service("vacuum/start", entity_id="vacuum.xiaomi_vacuum_cleaner")
          self.notify("Starting vacuum")
          self.log("Starting vacuum")

    self.log("Robot %s, dnd active %d, next %ds, until clean %ds" % (str(isRobotOn), self.dnd_active(), self.next_run, self.time_until_consider_cleaned))
    self.run_in(self.callback, SAMPLE_TIME)
