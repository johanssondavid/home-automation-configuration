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
    self.log("initialize")
    self.lamp_state_on = self.get_state("light.osram_plug1") == "on"
    self.log("lamp_state_on: " + str(self.lamp_state_on))

    # Create some callbacks
    self.listen_event(self.mode_event, "MODE_CHANGE")
    self.listen_event(self.deconz_event_cb, "deconz_event")
    self.listen_event(self.scene_change_cb, "SCENE")

    self.listen_state(self.everyone_left_home_cb, "group.all_devices", old = "home", new = "not_home")
    self.listen_state(self.someone_came_home_cb, "group.all_devices", old = "not_home", new = "home")

    self.listen_state(self.motion_cb, "binary_sensor.tradfri_motion_sensor__3")
    self.listen_state(self.motion_cb, "binary_sensor.tradfri_motion_sensor__4")

    # alarms
    runtime = datetime.time(5, 15, 0)
    self.run_daily(self.morning_cb, runtime)

    # sunset/sunrise
    self.run_at_sunrise(self.sunrise_cb, offset=1800)
    self.run_at_sunset(self.sunset_cb, offset=-1800)

    self.motion_timer = 0
    self.color_cycle_value = 0

    self.scene = 0

  def scene_off(self):
    self.scene = 0
    self.lamp_state_on = False
    self.turn_on("scene.scene_0")

  def scene_1(self):
    self.scene = 1
    self.lamp_state_on = True
    self.turn_on("scene.scene_1")

  def scene_2(self):
    self.scene = 2
    self.lamp_state_on = True
    self.turn_on("scene.scene_2")

  def scene_3(self):
    self.scene = 3
    self.lamp_state_on = True
    self.turn_on("scene.scene_3")

  def scene_4(self):
    self.scene = 4
    self.lamp_state_on = True
    self.turn_on("scene.scene_4")

  def scene_5(self):
    self.scene = 5
    self.lamp_state_on = True
    self.turn_on("scene.scene_5")


  def get_mode(self):
    return self.get_state("input_select.house_mode")

  # CALLBACKS
  def motion_cb(self, entity, attribute, old, new, kwargs):
    if new == "on":
      self.log("Motion detected from sensor: " + entity)
      if self.get_mode() == "Night":
        self.motion_timer = time.time() + MOTION_DELAY
        self.run_in(self.lights_off_after_motion, MOTION_DELAY + 5)
        self.turn_on("scene.scene_night")

      morning = (self.get_mode() == "Morning") and not(self.lights_automation_on())
      evening = (self.get_mode() == "Evening") and not(self.someone_is_home())
      if morning or evening:
        self.scene_3()

  def lights_off_after_motion(self, kwargs):
    if (self.motion_timer < time.time()) and (self.get_mode() == "Night"):
      self.scene_off()
    
  def everyone_left_home_cb(self, entity, attribute, old, new, kwargs):
    self.log("eveyone left home")
    self.scene_off()

  def someone_came_home_cb(self, entity, attribute, old, new, kwargs):
    self.log("someone came home")
    if (self.get_mode() == "Morning") or (self.get_mode() == "Evening"):
      self.scene_3()

  def morning_cb(self, kvwargs):
    self.morning()

  def sunrise_cb(self, kwargs):
    self.day()

  def sunset_cb(self, kwargs):
    self.evening()
    
  def mode_event(self, event_name, data, kwargs):
    mode = data["mode"]

    if mode == "Morning":
      self.morning()
    elif mode == "Day":
      self.day()
    elif mode == "Evening":
      self.evening()
    elif mode == "Night":
      self.night()

    self.log("mode_event: " + self.get_mode())

  def scene_change_cb(self, event_name, data, kwargs):
    increment = data["increment"]
    self.log("increment " + str(increment) + " pressed")

    if increment == "up":
      self.cycle_scene(1)
    if increment == "down":
      self.cycle_scene(-1)

  def deconz_event_cb(self, event_name, data, kwargs):
    event =  data["event"]
    self.log("button " + str(event) + " pressed")

    if event == 1002:
      self.toggle_lamps()
    elif event == 2002:
      self.cycle_scene(1)
    elif event == 3002:
      self.cycle_scene(-1)
    elif event == 5002:
      self.cycle_color(1)
    elif event == 4002:
      self.cycle_color(-1)

  def delay_off_night_cb(self, kwargs):
    self.scene_off()

  #
  # HELP FUNCTIONS
  #
  def someone_is_home(self):
    return (self.get_state(entity_id="group.all_devices") == "home") or not(self.automations_on())

  def automations_on(self):
    return self.get_state(entity_id="input_boolean.automations_off") == "off"

  def lights_automation_on(self):
    return self.get_state(entity_id="input_boolean.lights_automation") == "on" and self.automations_on()

  def vacuum_automation_on(self):
    return self.get_state(entity_id="input_boolean.vacuum_automation") == "on" and self.automations_on()

  def wakeuplight_automation_on(self):
    return self.get_state(entity_id="input_boolean.wakeuplight_automation") == "on" and self.automations_on()

  def cycle_color(self, value):
    self.color_cycle_value += value

    self.color_cycle_value = max(self.color_cycle_value, 0)
    self.color_cycle_value = min(self.color_cycle_value, 5)

    val = self.color_cycle_value 

    if val == 0:
      self.turn_off("light.hue_rgb1")
    elif val == 1:
      self.turn_on("light.hue_rgb1", brightness_pct=100, color_temp=500)
    elif val == 2:
      self.turn_on("light.hue_rgb1", brightness_pct=100, color_temp=319)
    elif val == 3:
      self.turn_on("light.hue_rgb1", brightness_pct=100, rgb_color = [255,0,0])
    elif val == 4:
      self.turn_on("light.hue_rgb1", brightness_pct=100, rgb_color = [0,255,0])
    elif val == 5:
      self.turn_on("light.hue_rgb1", brightness_pct=100, rgb_color = [0,0,255])
    else:
      pass

  def cycle_scene(self, value):
    self.scene += value

    self.scene = max(self.scene, 0)
    self.scene = min(self.scene, 5)

    val = self.scene 

    if val == 0:
      self.scene_off()
    elif val == 1:
      self.scene_1()
    elif val == 2:
      self.scene_2()
    elif val == 3:
      self.scene_3()
    elif val == 4:
      self.scene_4()
    elif val == 5:
      self.scene_5()
    else:
      pass

  def toggle_lamps(self):
      if self.lamp_state_on:
        self.turn_off("light.osram_plug1")
        self.turn_off("group.all_lights")
        self.turn_off("light.hue_rgb1")
      else:
        self.turn_on("light.osram_plug1")
        self.turn_on("group.all_lights")
        self.turn_on("light.hue_rgb1")
      self.lamp_state_on = not(self.lamp_state_on)
  
  def morning(self):
    self.log("Switching mode to Morning")
    self.select_option("input_select.house_mode", "Morning")
    
    self.log(datetime.datetime.today().weekday())

    if datetime.datetime.today().weekday() < 5 and self.wakeuplight_automation_on():
      self.turn_on("light.hue_rgb1", transition = 1800, brightness_pct=80, color_temp=319)

  def day(self):
    self.log("Switching mode to Day")
    self.select_option("input_select.house_mode", "Day")

    self.scene_off()

  def evening(self):
    self.log("Switching mode to Evening")
    self.select_option("input_select.house_mode", "Evening")

    #if self.someone_is_home():
    #  self.scene_3()

  def night(self):
    self.log("Switching mode to Night")
    self.select_option("input_select.house_mode", "Night")

    self.turn_off("light.osram_plug1")
    self.run_in(self.delay_off_night_cb, 12)
