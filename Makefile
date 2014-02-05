SHELL := /bin/bash
# RED :='\e[0;31m'
# echo "${RED}

deploy: clean install-utilities build run

clean:
	@echo "Cleaning up containers"
	-@docker stop elasticsearch_server 2>/dev/null || true
	-@docker rm elasticsearch_server 2>/dev/null || true
	-@docker stop postgresql_server 2>/dev/null || true
	-@docker rm postgresql_server 2>/dev/null || true

run: clean run-elasticsearch run-postgresql

stop:
	docker stop elasticsearch_server

build: build-ubuntu-base build-elasticsearch build-postgresql

build-postgresql:
	docker build -t postgresql_server github.com/GlobAllomeTree/docker-postgresql

build-ubuntu-base:
	docker build -t ubuntu_base github.com/GlobAllomeTree/docker-ubuntu-base

build-web-server:
	docker build -t web_server .

# run-mysql:
# 	sudo mkdir -p /data/
# 	sudo mkdir -p /data/mysql
# 	docker run -d -name mysql_server -p 3306:3306 -v /data/mysql:/var/lib/mysql mysql

build-elasticsearch:
	docker build -t elasticsearch_server github.com/GlobAllomeTree/docker-elasticsearch



run-elasticsearch:
	sudo mkdir -p /opt/
	sudo mkdir -p /opt/data/
	sudo mkdir -p /opt/data/elasticsearch
	docker run -d -name elasticsearch_server -p 9200:9200 -v /opt/data/elasticsearch:/var/lib/elasticsearch elasticsearch_server

run-elasticsearch-bash:
	-@docker stop elasticsearch_server_bash 2>/dev/null || true
	-@docker rm elasticsearch_server_bash 2>/dev/null || true
	#https://github.com/dotcloud/docker/issues/514
	#dpkg-divert --local --rename --add /sbin/mknod && ln -s /bin/true /sbin/mknod
	docker run -i -t -name elasticsearch_server_bash -p 9200:9200 -v /opt/data/elasticsearch:/var/lib/elasticsearch elasticsearch_server /bin/bash

run-postgresql:
	docker run -d -p 5432:5432 -e POSTGRESQL_USER=docker -e POSTGRESQL_PASS=docker -e POSTGRESQL_DB=docker postgresql_server


run-web-server:
#   need a bit of editing
#	docker run -d -name web_server -link mysql_server:db -p 8081:80 demo_server 

stop-web-server:
	docker stop web_server

dump-globallometree-database:
	./server/export_globallometree_database.sh 



###### LOCAL UTILITIES ############### 

install-utilities:
	sudo apt-get install -y git 

build-postgresql-local:
	docker build -t postgresql_server /home/vagrant/synced/docker-postgresql

build-elasticsearch-local:
	docker build -t elasticsearch_server /home/vagrant/synced/docker-elasticsearch

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



