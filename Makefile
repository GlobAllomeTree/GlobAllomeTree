#SHELL := /bin/bash
deploy: clean install-utilities build

clean:
	@echo "Cleaning up containers"
	-@docker stop elasticsearch_server 2>/dev/null || true
	-@docker rm elasticsearch_server 2>/dev/null || true

run: clean run-elasticsearch

stop:
	docker stop elasticsearch_server

build: build-ubuntu-base

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

run-web-server:
#   need a bit of editing
#	docker run -d -name web_server -link mysql_server:db -p 8081:80 demo_server 

stop-web-server:
	docker stop web_server

dump-globallometree-database:
	./server/export_globallometree_database.sh 

install-utilities:
	sudo apt-get install -y git 