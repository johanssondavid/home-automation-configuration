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
```
sudo apt-get install python3-pip python3-venv
```

Add an account for Home Assistant called homeassistant. Since this account is only for running Home Assistant the extra arguments of -rm is added to create a system account and create a home directory.
```
sudo useradd -rm homeassistant
```

Next we will create a directory for the installation of Home Assistant and change the owner to the homeassistant account.
```
cd /srv
sudo mkdir homeassistant
sudo chown homeassistant:homeassistant homeassistant
```

Next up is to create and change to a virtual environment for Home Assistant. This will be done as the homeassistant account.
```
sudo su -s /bin/bash homeassistant
cd /srv/homeassistant
python3 -m venv .
source bin/activate
```

Once you have activated the virtual environment you will notice the prompt change and then you can install Home Assistant (don't be afraid of the errors, seems to work anyway).
```
pip3 install homeassistant
```

Checkout the configuration from github
```
cd ~
git init
git remote add origin https://github.com/johanssondavid/home-automation-configuration
git fetch
git checkout origin/master
```

```
sudo nano -w /etc/systemd/system/home-assistant@homeassistant.service
```
```
[Unit]
Description=Home Assistant
After=network-online.target

[Service]
Type=simple
User=%i
ExecStart=/srv/homeassistant/bin/hass -c "/home/homeassistant/.homeassistant"

[Install]
WantedBy=multi-user.target
```

You need to reload systemd to make the daemon aware of the new configuration.
```
sudo systemctl --system daemon-reload
```

To have Home Assistant start automatically at boot, enable the service.
```
sudo systemctl enable home-assistant@homeassistant
```

To disable the automatic start, use this command.
```
sudo systemctl start home-assistant@homeassistant
```

Check log
```
sudo journalctl -f -u home-assistant@homeassistant
```

deconz https://github.com/dresden-elektronik/deconz-rest-plugin

```
wget https://www.dresden-elektronik.de/deconz/ubuntu/beta/deconz-2.04.99-qt5.deb
sudo dpkg -i deconz-2.04.99-qt5.deb
sudo apt-get install -f
sudo vim /etc/systemd/system/deconz.service
# Set user=root, bad idea?
sudo systemctl daemon-reload
sudo systemctl enable deconz
```


Configure dexonz in the gui. Follow the instructions (unlock gateway in deconz)



https://home-assistant.io/docs/installation/raspberry-pi/
https://home-assistant.io/docs/autostart/systemd/
