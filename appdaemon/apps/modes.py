import appdaemon.plugins.hass.hassapi as hass
import datetime
import appdaemon
import time

MOTION_DELAY = 90
DIMMER_STEP = 10

## IKEA
# kall 247
# medium 367
# varm 455

## Philips
# kall 153
# medium 319
# varm 500

class Modes(hass.Hass):
  def initialize(self):
    self.listen_event(self.deconz_event_cb, "deconz_event")

  def deconz_event_cb(self, event_name, data, kwargs):
    event =  data["event"]
    id = data["id"]

    if id == "tradfri_on_off_switch" and event == 2002:
        self.turn_off("switch.osram_plug1")
        self.turn_off("light.group_1")
        self.turn_off("light.hue_rgb1")
    elif id == "tradfri_on_off_switch" and event == 1002:
        self.turn_on("switch.osram_plug1")
        self.turn_on("light.group_1")
        self.turn_on("light.hue_rgb1")
    else:
        self.log("event_name: " + str(event_name))
        self.log("data: " + str(data))