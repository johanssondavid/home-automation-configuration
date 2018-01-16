import appdaemon.appapi as appapi

#
# Hello World App
#
# Args:
#

class TVReceiver(appapi.AppDaemon):

  def initialize(self):
    self.log("tv initialize")

    self.listen_state(self.tv_on, "binary_sensor.tv", old = "off", new = "on")
    self.listen_state(self.tv_off, "binary_sensor.tv", old = "on", new = "off")

  def tv_on(self, entity, attribute, old, new, kwargs):
    self.turn_on("switch.receiver")
    self.log("tv on")

  def tv_off(self, entity, attribute, old, new, kwargs):
    self.turn_off("switch.receiver")
    self.log("tv off")

