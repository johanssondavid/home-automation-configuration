import appdaemon.appapi as appapi
import datetime
import appdaemon
import time

class Advent(appapi.AppDaemon):

  def initialize(self):
    self.log("Advent starting ...")

    # sunset/sunrise
    self.run_at_sunrise(self.sunrise_cb, offset=1800)
    self.run_at_sunset(self.sunset_cb, offset=-1800)

    # mode change
    self.listen_event(self.mode_event, "MODE_CHANGE")

  def sunrise_cb(self, kwargs):
    self.turn_off("switch.advent_kok")

  def sunset_cb(self, kwargs):
    self.turn_on("switch.advent_kok")
    self.turn_on("switch.advent_vardagsrum")

  def mode_event(self, event_name, data, kwargs):
    mode = data["mode"]

    if mode == "Night":
      self.turn_off("switch.advent_vardagsrum")
  
