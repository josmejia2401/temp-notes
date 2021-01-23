# temp-notes
in react js


### instalación en windows
1. instalador GO - https://golang.org/doc/install
2. go get -u all
3. go get -v ./...    or    3. go get -d -v ./...
4. go build *go
5. go run *go

### Python
pip3 install -r requirements.txt

## Build docker sin cache
sudo docker-compose up --build --force-recreate
## Ejecutar docker sin bloqueo sin cache
sudo docker-compose -d -f docker-compose.yml up --force-recreate
## Comparibiulidad con recursos maquina (cpu, memoria)
sudo docker-compose --compatibility -f docker-compose.yml up

## Para ejecutar docker-compose compatible con deploy
sudo docker stack deploy --compose-file="docker-compose.yml" stack
## Ejecutar docker con bloqueo
sudo docker-compose -f docker-compose.yml up
## Docker estadisticas
sudo docker stats
## Docker comandos
sudo docker stop $(sudo docker container ls -q)
sudo docker container rm $(sudo docker container ls -q)
sudo docker image rm $(sudo docker image ls -q)
sudo docker volume rm $(sudo docker volume ls -q --filter dangling=true)
sudo docker system prune --all
## Docker
sudo service docker restart
sudo service docker start
sudo service docker stop


## Abrir puerto
sudo systemctl status ufw 
sudo ufw enable
sudo ufw allow 8080/tcp
# ftp
sudo ufw allow 21
# sftp
sudo ufw allow 22
# remover regla 8080
sudo ufw deny 8080
# reset
sudo ufw reset
# disable
sudo ufw disable
# status
sudo ufw status