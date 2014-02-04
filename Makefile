#SHELL := /bin/bash
deploy: clean install-utilities build

clean:
	@echo "Cleaning up containers"
	-@docker stop elasticsearch_server 2>/dev/null || true
	-@docker rm elasticsearch_server 2>/dev/null || true

run: clean run-elasticsearch

stop:
	docker stop elasticsearch_server

build: build-ubuntu-base build-elasticsearch

build-ubuntu-base:
	docker build -t ubuntu_base github.com/GlobAllomeTree/docker-ubuntu-base

build-web-server:
	docker build -t web_server .

# run-mysql:
# 	sudo mkdir -p /data/
# 	sudo mkdir -p /data/mysql
# 	docker run -d -name mysql_server -p 3306:3306 -v /data/mysql:/var/lib/mysql mysql

run-web-server:
#   need a bit of editing
#	docker run -d -name web_server -link mysql_server:db -p 8081:80 demo_server 

stop-web-server:
	docker stop web_server

dump-globallometree-database:
	./server/export_globallometree_database.sh 

install-utilities:
	sudo apt-get install -y git 