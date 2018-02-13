# home-automation-configuration
My home assistant configuration

I started running on a Raspberry pi 2 but found it unstable and slow. Instead installed in on a virtual machine running Ubuntu 16.04 LTS

## HW
* Virtual machine
* Conbee USB stick
* ESP8266 with 433 mhz transmitter
* IKEA Trådfri lamps
* ~~IKEA GW~~ substituted with conbee :thumbsup:
* IKEA Trådfri motion sensors
* IKEA Trådfri remote control
* Philips Hue RGB Lamp
* Logitech harmony remote

## SW
* Home Assistant
* AppDaemon
* ~~Node red~~ not needed with newer Home Assistant :thumbsup:
* Deconz
* HA Bridge


# Installation

## Home Assistant
* https://home-assistant.io/docs/installation/raspberry-pi/
* https://home-assistant.io/docs/autostart/systemd/

Install the dependencies.
```
sudo apt-get install python3-pip python3-venv autoconf nmap
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
pip3 install DTLSSocket
```

Checkout the configuration from github
```
cd ~
git init
git remote add origin https://github.com/johanssondavid/home-automation-configuration
git fetch
git checkout origin/master
```

I had to ad a delay before starting Home Assistant so deconz had time to start before. After and Wants was not enough.
```
sudo vim /etc/systemd/system/home-assistant@homeassistant.service
```
```
[Unit]
Description=Home Assistant
After=network-online.target

[Service]
ExecStartPre=/bin/sleep 30
Type=simple
User=%i
ExecStart=/srv/homeassistant/bin/hass -c "/home/homeassistant/.homeassistant"
After=deconz
Wants=deconz

[Install]
WantedBy=multi-user.target
```

```
sudo systemctl --system daemon-reload
sudo systemctl enable home-assistant@homeassistant
sudo systemctl start home-assistant@homeassistant
```

Check log
```
sudo journalctl -f -u home-assistant@homeassistant
```

## deconz
* https://github.com/dresden-elektronik/deconz-rest-plugin
* https://github.com/dresden-elektronik/deconz-rest-plugin/issues/274

```
wget https://www.dresden-elektronik.de/deconz/ubuntu/beta/deconz-2.04.99-qt5.deb
sudo dpkg -i deconz-2.04.99-qt5.deb
sudo apt-get install -f
sudo vim /etc/systemd/system/deconz.service
# Set user=root, bad idea?
# Set --upnp=0
sudo systemctl daemon-reload
sudo systemctl enable deconz
```


Configure deconz in the gui. Follow the instructions (unlock gateway in deconz)


## Appdaemon
* http://appdaemon.readthedocs.io/en/latest/INSTALL.html
```
sudo pip3 install 'appdaemon<3.0'
```

```
sudo vim /etc/systemd/system/appdaemon@appdaemon.service
```
```
[Unit]
Description=AppDaemon
After=home-assistant@homeassistant.service
[Service]
Type=simple
User=homeassistant
ExecStart=/usr/local/bin/appdaemon -c /home/homeassistant/appdaemon
[Install]
WantedBy=multi-user.target
```

```
sudo systemctl daemon-reload
sudo systemctl enable appdaemon@appdaemon.service --now
```


## HA-Bridge
* https://github.com/bwssytems/ha-bridge
* https://www.digitalocean.com/community/tutorials/how-to-install-java-with-apt-get-on-ubuntu-16-04

```
sudo apt-get install default-jre
sudo su -s /bin/bash homeassistant
cd
mkdir habridge
cd habridge
wget https://github.com/bwssytems/ha-bridge/releases/download/v5.1.0/ha-bridge-5.1.0.jar
exit
sudo vim /etc/systemd/system/habridge.service
```

```
[Unit]
Description=HA Bridge
Wants=network.target
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/homeassistant/habridge
ExecStart=/usr/bin/java -jar -Dconfig.file=/home/pi/habridge/data/habridge.config /home/pi/habridge/ha-bridge-5.1.0.jar

[Install]
WantedBy=multi-user.target
```

```
sudo systemctl daemon-reload
sudo systemctl enable habridge.service
sudo systemctl start habridge.service
```


