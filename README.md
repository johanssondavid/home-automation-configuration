# My home automation setup and installation instructions
Hello docker! :thumbsup:

## Todo
* Appdaemon 3

## Installation
0. Install ubuntu

1. Install docker - https://docs.docker.com/install/linux/docker-ce/ubuntu/
```
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
sudo apt-get update
sudo apt-get install docker-ce=17.12.0~ce-0~ubuntu
sudo systemctl enable docker
sudo docker login   
```
2. Install docker composer - https://docs.docker.com/compose/install/
```
sudo apt-get install python3-pip
sudo pip3 install docker-compose
```

3. Install portainer - https://portainer.io/install.html
```
sudo docker volume create portainer_data
sudo docker run -d -p 9000:9000 -v /var/run/docker.sock:/var/run/docker.sock --name portainer --restart always -v portainer_data:/data portainer/portainer
```

4. Fetch from git
```
cd
git clone https://github.com/johanssondavid/home-automation-configuration.git
cd home-automation-configuration/
mkdir home-automation-configuration/appdaemon/compiled            # obsolete ?
mkdir home-automation-configuration/appdaemon/compiled/css        # obsolete ?
mkdir home-automation-configuration/appdaemon/compiled/javascript # obsolete ?
```
5. (Re)create secrets.yaml files
6. Restore deconz files
6. Start docker compose

```
cd ~/home-automation-configuration/docker_compose/
sudo docker-compose up -d
```


## Useful commands

### deconz create api key
```
curl http://localhost:8080/api -d '{"devicetype": "home assistant"}'
```

### InfluxDB & Grafana
```
docker run -d \
--name="influxdb" \
--restart always \
-p 8086:8086 \
-p 8083:8083 \
-v /volume1/docker/influxdb/:/var/lib/influxdb \
influxdb
```

```
sudo docker run -d -p 3000:3000 --name="grafana" --restart always -v /home/david/data/grafana:/var/lib/grafana grafana/grafana:6.0.2
```

Grafana settings
172.17.0.5
d home_assistant
u home-assistant
p home_assistant


### ddclient
```
sudo docker run -d --name ddclient -v /home/david/data/ddclient:/config --restart unless-stopped linuxserver/ddclient
```

### Open VPN
```
sudo docker volume create --name openvpn_data
sudo docker run -v openvpn_data:/etc/openvpn kylemanna/openvpn ovpn_genconfig -u udp://<server> -2 -C AES-256-GCM
sudo docker run -v openvpn_data:/etc/openvpn --rm -it kylemanna/openvpn ovpn_initpki
#sudo docker run -v openvpn_data:/etc/openvpn --rm -it kylemanna/openvpn easyrsa build-ca
sudo docker run -v openvpn_data:/etc/openvpn --rm -it kylemanna/openvpn easyrsa build-client-full <user>
sudo docker run -v openvpn_data:/etc/openvpn --rm -it kylemanna/openvpn ovpn_otp_user <user>
sudo docker run -v openvpn_data:/etc/openvpn -d -p 1194:1194/udp --name openvpn --cap-add=NET_ADMIN --restart always kylemanna/openvpn
sudo docker run -v openvpn_data:/etc/openvpn --rm -it kylemanna/openvpn easyrsa build-client-full <user>_client nopass
sudo docker run -v openvpn_data:/etc/openvpn --rm -it kylemanna/openvpn ovpn_getclient <user>_client > <user>_client.ovpn

```
* https://ruimarinho.github.io/post/configuring-a-secure-openvpn-2-4-server-with-docker/
* https://toub.es/2018/02/15/low-cost-vpn-solution-with-two-factor-authentication-on-a-raspberry-pi/
