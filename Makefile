SHELL := /bin/bash

#TODO: read in variables from the environment if they are already set
POSTGRESQL_USER := 'globallometree'
POSTGRESQL_PASS := 'globallometree'
POSTGRESQL_DB := 'globallometree'

deploy: clean install-utilities build run

clean:
	@echo "Cleaning up containers"
	-@docker stop elasticsearch_server 2>/dev/null || true
	-@docker rm elasticsearch_server 2>/dev/null || true
	-@docker stop postgresql_server 2>/dev/null || true
	-@docker rm postgresql_server 2>/dev/null || true
	-@docker stop web_server 2>/dev/null || true
	-@docker rm web_server 2>/dev/null || true

run: clean run-elasticsearch run-postgresql run-web-server

stop:
	docker stop web_server
	docker stop elasticsearch_server
	docker stop postgresql_server

build: build-ubuntu-base build-elasticsearch build-postgresql build-web-server

build-postgresql:
	docker build -t postgresql_server_image github.com/GlobAllomeTree/docker-postgresql

build-ubuntu-base:
	docker build -t ubuntu_base github.com/GlobAllomeTree/docker-ubuntu-base

vbuild-web-server:
	docker build -t web_server_image .


build-elasticsearch:
	docker build -t elasticsearch_server_image github.com/GlobAllomeTree/docker-elasticsearch


run-elasticsearch:
	sudo mkdir -p /opt/
	sudo mkdir -p /opt/data/
	sudo mkdir -p /opt/data/elasticsearch
	docker run -d -name elasticsearch_server -p 9200:9200 -v /opt/data/elasticsearch:/var/lib/elasticsearch elasticsearch_server_image


run-elasticsearch-bash:
	-@docker stop elasticsearch_server_bash 2>/dev/null || true
	-@docker rm elasticsearch_server_bash 2>/dev/null || true
	docker run -i -t -name elasticsearch_server_bash -p 9200:9200 -v /opt/data/elasticsearch:/var/lib/elasticsearch elasticsearch_server_image /bin/bash


run-postgresql:
	sudo mkdir -p /opt/
	sudo mkdir -p /opt/data/
	sudo mkdir -p /opt/data/postgresql
	docker run -d -name postgresql_server -p 5432:5432 -v /opt/data/postgresql:/var/lib/postgresql -e POSTGRESQL_USER=${POSTGRESQL_USER} -e POSTGRESQL_PASS=${POSTGRESQL_PASS} -e POSTGRESQL_DB=${POSTGRESQL_DB} postgresql_server_image


run-web-server:
	docker run -d -name web_server -link postgresql_server:DB -link elasticsearch_server:ES -v /home/vagrant/synced/globallometree:/home/docker/code  -p 8082:80 -e POSTGRESQL_USER=${POSTGRESQL_USER} -e POSTGRESQL_PASS=${POSTGRESQL_PASS} -e POSTGRESQL_DB=${POSTGRESQL_DB} web_server_image 

stop-web-server:
	docker stop web_server


dump-globallometree-database:
	./server/export_globallometree_database.sh 



###### LOCAL UTILITIES ############### 

install-utilities:
	sudo apt-get install -y git 
	sudo apt-get install -y postgresql-client

build-postgresql-local:
	docker build -t postgresql_server_image /home/vagrant/synced/docker-postgresql

build-elasticsearch-local:
	docker build -t elasticsearch_server_image /home/vagrant/synced/docker-elasticsearch

git-pull-all:
	@echo
	@tput setaf 6 && echo "--------------- GlobAllomeTree ----------------" && tput sgr0
	git pull
	
	@echo
	@tput setaf 6 && echo "--------------- PostgreSQL Docker ----------------" && tput sgr0
	cd ../docker-postgresql && git pull
	
	@echo
	@tput setaf 6 && echo "--------------- ElasticSearch Docker ----------------" && tput sgr0
	cd ../docker-elasticsearch && git pull
	
	@echo
	@tput setaf 6 && echo "--------------- Ubuntu Base Docker ----------------" && tput sgr0
	cd ../docker-ubuntu-base && git pull

git-push-all:
	@echo
	@tput setaf 6 && echo "--------------- GlobAllomeTree ----------------" && tput setaf 0
	git push
	
	@echo
	@tput setaf 6 && echo "--------------- PostgreSQL Docker ----------------" && tput setaf 0
	cd ../docker-postgresql && git push
	
	@echo
	@tput setaf 6 && echo "--------------- ElasticSearch Docker ----------------" && tput setaf 0
	cd ../docker-elasticsearch && git push
	
	@echo
	@tput setaf 6 && echo "--------------- Ubuntu Base Docker ----------------" && tput setaf 0
	cd ../docker-ubuntu-base && git push

git-status-all:
	@echo
	@tput setaf 6 && echo "--------------- GlobAllomeTree ----------------" && tput sgr0
	git status
	
	@echo
	@tput setaf 6 && echo "--------------- PostgreSQL Docker ----------------" && tput sgr0
	cd ../docker-postgresql && git status
	
	@echo
	@tput setaf 6 && echo "--------------- ElasticSearch Docker ----------------" && tput sgr0
	cd ../docker-elasticsearch && git status
	
	@echo
	@tput setaf 6 && echo "--------------- Ubuntu Base Docker ----------------" && tput sgr0
	cd ../docker-ubuntu-base && git status



