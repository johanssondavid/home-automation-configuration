# home-automation-configuration
My home assistant configuration

HW
* Rasperry Pi 2
* Conbee USB stick
* ESP8266 with 433 mhz transmitter
* IKEA Trådfri lamps
* IKEA GW
* IKEA Trådfri motion sensors
* IKEA Trådfri remote control
* Philips Hue RGB Lamp
* Logitech harmony remote

SW
* Home Assistant
* AppDaemon
* Node red
* Deconz
* HA Bridge


Installation

Install the dependencies.
$ sudo apt-get install python3-pip python3-venv

Add an account for Home Assistant called homeassistant. Since this account is only for running Home Assistant the extra arguments of -rm is added to create a system account and create a home directory.
$ sudo useradd -rm homeassistant

Next we will create a directory for the installation of Home Assistant and change the owner to the homeassistant account.
$ cd /srv
$ sudo mkdir homeassistant
$ sudo chown homeassistant:homeassistant homeassistant

Next up is to create and change to a virtual environment for Home Assistant. This will be done as the homeassistant account.

$ sudo su -s /bin/bash homeassistant
$ cd /srv/homeassistant
$ python3 -m venv .
$ source bin/activate

Once you have activated the virtual environment you will notice the prompt change and then you can install Home Assistant (don't be afraid of the errors, seems to work anyway).

(homeassistant) homeassistant@raspberrypi:/srv/homeassistant $ pip3 install homeassistant

