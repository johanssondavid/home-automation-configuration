import appdaemon.appapi as appapi
import datetime
import appdaemon
import time

MOTION_DELAY = 90
DIMMER_STEP = 10


class LightDimmer():
  def __init__(self, appdaemon, entity_id):
    self.appdaemon = appdaemon
    self.entity_id = entity_id
    self.current_brightness = 254
    self.sleep = 1

  def set_color(self, rgb):
    self.appdaemon.turn_on(self.entity_id, rgb_color=rgb, brightness=self.current_brightness)

  def set_temp(self, temp):
    self.appdaemon.turn_on(self.entity_id, color_temp=temp, brightness=self.current_brightness)

  def set_brightness(self, brightness_percent):
    brightness = brightness_percent*(255/100)
    self.current_brightness = brightness
    self.requested_brightness = brightness
    self.appdaemon.turn_on(self.entity_id, brightness=brightness)

  def turn_off(self):
    self.appdaemon.turn_off(self.entity_id)

  def turn_on(self):
    self.appdaemon.turn_on(self.entity_id)

  def set_level_slow(self, brightness_percent, transition_time):
    brightness = brightness_percent*(255/100)

    self.requested_brightness = brightness

    diff = abs(self.current_brightness - self.requested_brightness)
    self.sleep = transition_time / (diff / DIMMER_STEP)

    self.local_update(None)

  def local_update(self, kwargs):
    if self.current_brightness < self.requested_brightness:
      self.current_brightness = min(self.requested_brightness, self.current_brightness + DIMMER_STEP)
    elif self.current_brightness > self.requested_brightness:
      self.current_brightness = max(self.requested_brightness, self.current_brightness - DIMMER_STEP)
    else:
      return

    self.appdaemon.turn_on(self.entity_id, brightness=self.current_brightness)
    self.appdaemon.run_in(self.local_update, self.sleep)


class Modes(appapi.AppDaemon):
  def initialize(self):
    # setup lamps
    self.light_1          = LightDimmer(self, "light.light_1")
    self.fonster1         = LightDimmer(self, "light.fonster1")
    self.fonster2         = LightDimmer(self, "light.fonster2")
    self.golvlampa        = LightDimmer(self, "light.golvlampa")
    self.koksfonster      = LightDimmer(self, "light.koksfonster")
    self.sanglampa        = LightDimmer(self, "light.sanglampa")
    self.fonster_sovrum   = LightDimmer(self, "light.fonster_sovrum")
    self.hall             = LightDimmer(self, "light.hall")


    #self.dimmertest2 = LightDimmer(self, "light.golvlampa")
    #self.dimmertest.set_level_slow(255)
    #self.dimmertest2.set_level_slow(255)

    #self.dimmertest2.set_brightness(0)
    #self.dimmertest2.set_brightness(10)
    #self.dimmertest2.set_level_slow(100, 600)
    #self.dimmertest.set_color([255,0,0])
    #self.dimmertest.set_temp(319)
    #self.dimmertest2.set_temp(367)

    ## IKEA
    # kall 247
    # medium 367
    # varm 455

    ## Philips
    # kall 153
    # medium 319
    # varm 500

    self.lamp_state_on = self.get_state("switch.livingroom_shelf") == "on"
    self.log("lamp_state_on: " + str(self.lamp_state_on))

    # Create some callbacks
    self.listen_event(self.mode_event, "MODE_CHANGE")
    self.listen_event(self.button_pressed_cb, "REMOTE_PRESSED")
    self.listen_event(self.harmony_pressed_cb, "HARMONY_PRESSED")

    self.listen_state(self.everyone_left_home_cb, "group.all_devices", old = "home", new = "not_home")
    self.listen_state(self.someone_came_home_cb, "group.all_devices", old = "not_home", new = "home")

    self.listen_state(self.motion_cb, "sensor.motion")
    self.listen_state(self.motion_cb, "sensor.motion_2")

    # alarms
    runtime = datetime.time(5, 45, 0)
    self.run_daily(self.morning_cb, runtime)

    # sunset/sunrise
    self.run_at_sunrise(self.sunrise_cb, offset=1800)
    self.run_at_sunset(self.sunset_cb, offset=-1800)

    self.motion_timer = 0
    self.color_cycle_value = 0

    self.scene = 0

  def scene_off(self):
    self.scene = 0
    self.light_1.turn_off()
    self.turn_off("switch.livingroom_shelf")
    self.fonster1.turn_off()
    self.fonster2.turn_off()
    self.golvlampa.turn_off()
    self.koksfonster.turn_off()
    self.sanglampa.turn_off()
    self.fonster_sovrum.turn_off()
    self.hall.turn_off()

  def scene_1(self):
    self.scene = 1
    self.light_1.turn_off()
    self.turn_off("switch.livingroom_shelf")
    self.fonster1.set_brightness(20)
    self.fonster2.turn_off()
    self.golvlampa.set_brightness(20)
    self.koksfonster.set_brightness(20)
    self.sanglampa.turn_off()
    self.fonster_sovrum.turn_off()
    self.hall.set_brightness(20)

  def scene_2(self):
    self.scene = 2
    self.light_1.turn_off()
    self.turn_on("switch.livingroom_shelf")
    self.fonster1.set_brightness(50)
    self.fonster2.set_brightness(50)
    self.golvlampa.set_brightness(50)
    self.koksfonster.set_brightness(50)
    self.sanglampa.set_brightness(50)
    self.fonster_sovrum.set_brightness(50)
    self.hall.set_brightness(50)

  def scene_3(self):
    self.scene = 3
    self.light_1.set_brightness(25)
    self.turn_on("switch.livingroom_shelf")
    self.fonster1.set_brightness(75)
    self.fonster2.set_brightness(75)
    self.golvlampa.set_brightness(75)
    self.koksfonster.set_brightness(75)
    self.sanglampa.set_brightness(75)
    self.fonster_sovrum.set_brightness(75)
    self.hall.set_brightness(75)

  def scene_4(self):
    self.scene = 4
    self.light_1.set_brightness(60)
    self.turn_on("switch.livingroom_shelf")
    self.fonster1.set_brightness(100)
    self.fonster2.set_brightness(100)
    self.golvlampa.set_brightness(100)
    self.koksfonster.set_brightness(100)
    self.sanglampa.set_brightness(100)
    self.fonster_sovrum.set_brightness(100)
    self.hall.set_brightness(100)

  def scene_5(self):
    self.scene = 5
    self.light_1.set_brightness(100)
    self.turn_on("switch.livingroom_shelf")
    self.fonster1.set_brightness(100)
    self.fonster2.set_brightness(100)
    self.golvlampa.set_brightness(100)
    self.koksfonster.set_brightness(100)
    self.sanglampa.set_brightness(100)
    self.fonster_sovrum.set_brightness(100)
    self.hall.set_brightness(100)


  def get_mode(self):
    return self.get_state("input_select.house_mode")

  # CALLBACKS
  def motion_cb(self, entity, attribute, old, new, kwargs):
    if new == "1":
      if self.get_mode() == "Night":
        self.motion_timer = time.time() + MOTION_DELAY
        self.run_in(self.lights_off_after_motion, MOTION_DELAY + 5)
        self.koksfonster.set_brightness(20)
        self.hall.set_brightness(20)

      morning = (self.get_mode() == "Morning") and not(self.visitor_present())
      evening = (self.get_mode() == "Evening") and not(self.someone_is_home())
      if morning or evening:
        self.scene_3()

  def lights_off_after_motion(self, kwargs):
    if (self.motion_timer < time.time()) and (self.get_mode() == "Night"):
      self.koksfonster.turn_off()
      self.hall.turn_off()
    
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

  def harmony_pressed_cb(self, event_name, data, kwargs):
    button = data["button"]
    self.log("button " + str(button) + " pressed")

    if button == "1_on":
      self.cycle_scene(1)
    if button == "2_on":
      self.cycle_scene(-1)
    if button == "1_off":
      self.scene_4()
    if button == "2_off":
      self.scene_off()

  def button_pressed_cb(self, event_name, data, kwargs):
    button = data["button"]
    self.log("button " + str(button) + " pressed")

    if button == 1:
      self.toggle_lamps()
    elif button == 5:
      self.cycle_color(1)
    elif button == 4:
      self.cycle_color(-1)

  def delay_off_night_cb(self, kwargs):
    self.turn_off("group.all_lights")

  #
  # HELP FUNCTIONS
  #
  def someone_is_home(self):
    return (self.get_state(entity_id="group.all_devices") == "home") or self.visitor_present()

  def visitor_present(self):
    return self.get_state(entity_id="input_boolean.visitor_present") == "on"

  def cycle_color(self, value):
    self.color_cycle_value += value

    self.color_cycle_value = max(self.color_cycle_value, 0)
    self.color_cycle_value = min(self.color_cycle_value, 5)

    val = self.color_cycle_value 

    if val == 0:
      self.light_1.set_brightness(0)
    elif val == 1:
      self.light_1.set_brightness(100)
      self.light_1.set_temp(500)
    elif val == 2:
      self.light_1.set_temp(319)
    elif val == 3:
      self.light_1.set_color([255,0,0])
    elif val == 4:
      self.light_1.set_color([0,255,0])
    elif val == 5:
      self.light_1.set_color([0,0,255])
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
        self.turn_off("switch.livingroom_shelf")
        self.turn_off("group.all_lights")
        self.light_1.turn_off()
      else:
        self.turn_on("switch.livingroom_shelf")
        self.turn_on("group.all_lights")
        self.light_1.turn_on()
      self.lamp_state_on = not(self.lamp_state_on)
  
  def morning(self):
    self.log("Switching mode to Morning")
    self.select_option("input_select.house_mode", "Morning")
    self.notify("Switching mode to Morning")
    
    self.log(datetime.datetime.today().weekday())
    self.log(self.visitor_present())

    if datetime.datetime.today().weekday() < 5 and not(self.visitor_present()):
      self.light_1.set_brightness(2)
      self.light_1.set_level_slow(100, 1800)

  def day(self):
    self.log("Switching mode to Day")
    self.select_option("input_select.house_mode", "Day")
    self.notify("Switching mode to Day")

    self.turn_off("switch.livingroom_shelf")
    self.turn_off("group.all_lights")

  def evening(self):
    self.log("Switching mode to Evening")
    self.select_option("input_select.house_mode", "Evening")
    self.notify("Switching mode to Evening")

    if self.someone_is_home():
      self.turn_on("switch.livingroom_shelf")
      self.turn_on("group.all_lights")

  def night(self):
    self.log("Switching mode to Night")
    self.select_option("input_select.house_mode", "Night")
    self.notify("Switching mode to Night")

    self.turn_off("switch.livingroom_shelf")
    self.run_in(self.delay_off_night_cb, 12)
