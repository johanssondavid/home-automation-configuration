# home-automation-configuration
Bye bye old stuff. Hello docker


## deconz
```
sudo docker run -d --name="deconz" --net="host" -e TZ="Europe/Berlin" -p 8080:8080/tcp -v "/home/david/home-automation-configuration/deconz":"/root/.local/share/dresden-elektronik/deCONZ":rw --device /dev/ttyUSB0:/dev/ttyUSB0 joch/deconz
```

## HA Bridge
TODO

## Home Assistant
TODO
