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
## Docker 
sudo docker-compose --compatibility -f docker-compose.yml rm --all & sudo docker-compose --compatibility -f docker-compose.yml build --no-cache & sudo docker-compose --compatibility -f docker-compose.yml up --force-recreate
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
sudo ufw reject 8080
ufw delete 8080
# reset
sudo ufw reset
# disable
sudo ufw disable
# status
sudo ufw status
sudo ufw status verbose
# kill app port
kill -9 $(lsof -t -i:8080)
# Exponer puerto a interner
1. Descargar: https://ngrok.com/download
2. ./ngrok http 8080

./staqlab-tunnel 8080 hostname=sudo9


Buenos días,

Solicito amablemente configurar mi ruoter o modem para que exponga los puertos 8080, 9100, 9101, 9102, 9200, 9201, 9203, 9090 y 9091 a internet, esto con el fin de exponer mis aplicaciones web a la nube.

Los puertos 9090 y 9091 deben permitir el acceso desde el exterior (internet o nube) y redirigirlos a la IPv4 local 192.168.0.5 con los puertos descritos anteriormente (9090 y 9091)

Los puertos 8080 y 9100, 9101, 9102 deben permitir el acceso desde el exterior (internet o nube) y redirigirlos a la IPv4 local 192.168.0.6 con los puertos descritos anteriormente (8080, 9100, 9101, 9102)

Los puertos 9200, 9201, 9203 deben permitir el acceso desde el exterior (internet o nube) y redirigirlos a la IPv4 local 192.168.0.7 con los puertos descritos anteriormente (9200, 9201, 9203)

Muchas gracias,