# temp-notes
react js
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
# kill app port
kill -9 $(lsof -t -i:8080)
# Abrir puerto a Internet
1. En linux - Debe estar conectada por cable
- RED - Proxy de la Red - Manual - Proxy para HTTP: 127.0.0.1 8080