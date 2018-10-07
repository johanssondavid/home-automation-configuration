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
