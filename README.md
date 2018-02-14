# home-automation-configuration
Bye bye old stuff. Hello docker! :thumbsup:

## Todo list
* Appdaemon 3

## Installation
1. Install docker - https://docs.docker.com/install/linux/docker-ce/ubuntu/
2. Install portainer - https://portainer.io/install.html
3. Fetch from git
```
git clone ...
mkdir home-automation-configuration/appdaemon/compiled
mkdir home-automation-configuration/appdaemon/compiled/css
mkdir home-automation-configuration/appdaemon/compiled/javascript
```

4. (Re)create secrets.yaml files
5. Start the containers below

### deconz
```
sudo docker run -d --net=host --name deconz -e TZ="Europe/Berlin" -p 8080:8080/tcp -v "/home/david/home-automation-configuration/deconz":"/root/.local/share/dresden-elektronik/deCONZ":rw --device /dev/ttyUSB0:/dev/ttyUSB0 joch/deconz
```

### Home Assistant
```
sudo docker run -d --net=host --name homeassistant -v /home/david/home-automation-configuration/homeassistant:/config -v /etc/localtime:/etc/localtime:ro -p 8123:8123 homeassistant/home-assistant
```

### HA Bridge
```
sudo docker run -d --net=host --name ha-bridge -v /home/david/home-automation-configuration/habridge/data/:/bridge/data -p 8124:8080 bios/docker-alexa-ha-bridge
```

### AppDaemon
```
sudo docker run -d --net=host --name appdaemon -v /home/david/home-automation-configuration/appdaemon/:/conf -p 5050:5050 johanssondavid/appdaemon2
```
