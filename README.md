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

sudo docker-compose up -d
sudo docker-compose -f docker-compose.yml up

sudo docker stop $(sudo docker container ls -q)
sudo docker container rm $(sudo docker container ls -q)
sudo docker image rm $(sudo docker image ls -q)
sudo docker volume rm $(sudo docker volume ls -q --filter dangling=true)
sudo docker system prune --all

