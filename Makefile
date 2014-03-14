# Makefile for managing the GlobAllomeTree dockers

#  := evaluated later when run or used
#   = evaluated immediately when encountered by parser

SHELL := /bin/bash
POSTGRESQL_USER = globallometree
POSTGRESQL_PASS = globallometree
POSTGRESQL_DB   = globallometree
WEB_SERVER_PORT = 8082
ELASTICSEARCH_PORT = 9200
SECRET_KEY = secret

#DUMP_FILE is assumed to be in the one directory up from this file
DUMP_FILE = ../globallometree.import.sql.gz
PSQL = PGPASSWORD=$(POSTGRESQL_PASS) psql -U $(POSTGRESQL_USER) -h $(shell TAG=postgresql_server_image ./server/ip_for.sh)
PROJECT_ROOT := $(shell pwd)

#Create a file called Makefile.local to overide the above settings on a per server basis
-include Makefile.local

#This will get evaluated when used below
WEB_SERVER_BASE_ENV := -link postgresql_server:DB -link elasticsearch_server:ES -v ${PROJECT_ROOT}:/home/docker/code -e SECRET_KEY=${SECRET_KEY}  -e POSTGRESQL_USER=${POSTGRESQL_USER} -e POSTGRESQL_PASS=${POSTGRESQL_PASS} -e POSTGRESQL_DB=${POSTGRESQL_DB} 

deploy: clean install-utilities build init sleep10 run

build: build-ubuntu-base build-elasticsearch build-postgresql build-web-server

init: init-postgresql 

clean: clean-elasticsearch clean-postgresql clean-web-server	

run: clean run-elasticsearch run-postgresql run-web-server
	docker ps

stop: stop-web-server stop-elasticsearch stop-postgresql


run-cache-server:
	#http://ftp.gnu.org/old-gnu/Manuals/make-3.79.1/html_chapter/make_toc.html#TOC50
	cd ../docker-cache && $(MAKE) run

########################################### UTILITIES ############################################

sleep10:
	sleep 10

sleep20:
	sleep 20

echo-vars:
	@echo "PROJECT_ROOT = '${PROJECT_ROOT}'"
	@echo "POSTGRESQL_USER = '${POSTGRESQL_USER}'"
	@echo "POSTGRESQL_PASS = '${POSTGRESQL_PASS}'"
	@echo "POSTGRESQL_DB   = '${POSTGRESQL_DB}'"

########################################### UBUNTU BASE IMAGE #########################################

build-ubuntu-base:
	docker build -t ubuntu_base github.com/GlobAllomeTree/docker-ubuntu-base


########################################### WEB SERVER #########################################


clean-web-server:
	-@docker stop web_server 2>/dev/null || true
	-@docker rm web_server 2>/dev/null || true

build-web-server:
	docker build -t web_server_image .

run-web-server: clean-web-server
	#Run the webserver on port 8082
	docker run -d -name web_server -p ${WEB_SERVER_PORT}:80 ${WEB_SERVER_BASE_ENV} web_server_image

stop-web-server:
	docker stop web_server

run-web-server-debug:
	#Run a debug server on port 8083
	-@docker stop web_server_bash 2>/dev/null || true
	-@docker rm web_server_bash 2>/dev/null || true
	docker run -i -t -name web_server_bash -p 8083:8083 ${WEB_SERVER_BASE_ENV} web_server_image bash /home/docker/code/server/startup_bash.sh

attach-web-server:
	#Use lxc attach to attch to the webserver
	$(MAKE) dock-attach CONTAINER=web_server

django-manage:
	#Run manage.py 
	#Example)  django-manage COMMAND="collectstatic --noinput"
	-@docker stop django_manage 2>/dev/null || true
	-@docker rm django_manage 2>/dev/null || true
	docker run -i -t -name django_manage ${WEB_SERVER_BASE_ENV} -e COMMAND="${COMMAND}" web_server_image bash /home/docker/code/server/startup_manage.sh

django-runserver:
	$(MAKE) run-web-server-debug

django-collectstatic:
	$(MAKE) django-manage COMMAND="collectstatic --noinput"

django-rebuild-index:
	$(MAKE) django-manage COMMAND="rebuild_index --noinput"

#Graphing	
graph-all-models:
	$(MAKE) django-manage COMMAND="graph_models -a -o all_models.png"

graph-data-models:
	$(MAKE) django-manage COMMAND="graph_models taxonomy allometric_equations wood_densities locations common -x modified,created -o data_models_phase_2.png"

graph-p1-data-models:
	$(MAKE) django-manage COMMAND="graph_models data -o data_models_phase_1.png"



############################################# ELASTICSEARCH  #############################################

clean-elasticsearch:
	-@docker stop elasticsearch_server 2>/dev/null || true
	-@docker rm elasticsearch_server 2>/dev/null || true

build-elasticsearch:
	docker build -t elasticsearch_server_image github.com/GlobAllomeTree/docker-elasticsearch


run-elasticsearch: clean-elasticsearch
	sudo mkdir -p /opt/
	sudo mkdir -p /opt/data/
	sudo mkdir -p /opt/data/elasticsearch
	docker run -d -name elasticsearch_server -p ${ELASTICSEARCH_PORT}:9200 -v /opt/data/elasticsearch:/var/lib/elasticsearch elasticsearch_server_image


stop-elasticsearch:
	docker stop elasticsearch_server

run-elasticsearch-bash:
	-@docker stop elasticsearch_server_bash 2>/dev/null || true
	-@docker rm elasticsearch_server_bash 2>/dev/null || true
	docker run -i -t -name elasticsearch_server_bash -p ${ELASTICSEARCH_PORT}:9200 -v /opt/data/elasticsearch:/var/lib/elasticsearch elasticsearch_server_image /bin/bash



############################################# POSTGRES  #############################################

clean-postgresql:
	-@docker stop postgresql_server 2>/dev/null || true
	-@docker rm postgresql_server 2>/dev/null || true

build-postgresql:
	docker build -t postgresql_server_image github.com/GlobAllomeTree/docker-postgresql

init-postgresql: run-postgresql sleep10 create-db import-db stop-postgresql 

run-postgresql: clean-postgresql
	sudo mkdir -p /opt/
	sudo mkdir -p /opt/data/
	sudo mkdir -p /opt/data/postgresql
	docker run -d -name postgresql_server -p 5432:5432 -v /opt/data/postgresql:/var/lib/postgresql -e POSTGRESQL_USER=${POSTGRESQL_USER} -e POSTGRESQL_PASS=${POSTGRESQL_PASS} -e POSTGRESQL_DB=${POSTGRESQL_DB} postgresql_server_image

stop-postgresql:
	docker stop postgresql_server


#Force postgres to reinitialize everything which happens in the docker postgresql startup.sh script if db is not initialized
#TODO: Add a confirm here
delete-postgres-data-directory:
	sudo rm -rf /opt/data/postgresql 

#You must add the DUMP_FILE yourself and it should be a gzipped version of the GlobAllomeTree db
#This uses env vars to avoid the password prompt
#http://www.postgresql.org/docs/current/static/libpq-envars.html
#To use a different dump file, override the DUMP_FILE variable when calling Make
#ex) make import-db DUMP_FILE=../globallometree.import.sql.2.gz
#Note that $(PSQL) is defined at the beginning of the Makefile but evaluated when used below
import-db: 
	gunzip -c $(DUMP_FILE) | $(PSQL)

drop-db:
	echo "DROP DATABASE  IF EXISTS  ${POSTGRESQL_DB};" | $(PSQL) postgres 

create-db:
	echo "CREATE DATABASE ${POSTGRESQL_DB} OWNER ${POSTGRESQL_USER} ENCODING 'UTF8' TEMPLATE template0; " | $(PSQL) postgres

reimport-db: drop-db create-db import-db


dump-db:
	PGPASSWORD=$(POSTGRESQL_PASS) pg_dump -U $(POSTGRESQL_USER) -h $(shell TAG=postgresql_server_image ./server/ip_for.sh) $(POSTGRESQL_DB) | gzip > ../$(POSTGRESQL_DB).dump.`date +'%Y_%m_%d'`.sql.gz
	@echo "database exported to ../${POSTGRESQL_DB}.`date +'%Y_%m_%d'`.sql.gz"

#This does a full reset of postgres from a dump file
#To use a different dump file, override the DUMP_FILE variable when calling Make
#ex) make reset-postgresql DUMP_FILE=../globallometree.import.sql.2.gz
reset-postgresql: clean-postgresql delete-postgres-data-directory init-postgresql 
	$(MAKE) run-postgresql

get-postgresql-ip:
	@echo $(shell TAG=postgresql_server_image ./server/ip_for.sh)

#Hop into the shell and connect to the local database
psql-shell:
	$(PSQL)

#Utility to hop into the postgres admin shell
psql-admin-shell:
	$(PSQL) postgres




############################################ DOCKER SHORTCUTS ##########################################

stop-all-containers:
	docker stop `docker ps -notrunc -q`

#http://stackoverflow.com/questions/17236796/how-to-remove-old-docker-io-containers
#TODO: Add a confirm here
remove-all-containers:
	docker rm `docker ps -notrunc -a -q`

#http://jimhoskins.com/2013/07/27/remove-untagged-docker-images.html
#TODO: Add a confirm here
remove-untagged-images:	
	docker rmi `docker images | grep "^<none>" | awk "{print $3}"`

#http://techoverflow.net/blog/2013/10/22/docker-remove-all-images-and-containers/
#TODO: Add a confirm here
remove-all-images: 
	docker rmi $(docker images -q)

reset-docker: remove-all-containers remove-all-images
	#other things we can reset?

dock-attach:
	#Example) dock-attach CONTAINER=web_server
	#Example) make dock-attach CONTAINER=c1997df1e28
	sudo lxc-attach -n $(shell sudo docker inspect ${CONTAINER} | grep '"ID"' | sed 's/[^0-9a-z]//g') /bin/bash


########################### LOCAL UTILITIES FOR USE IN BUILDING IMAGES ############################ 

#	All of these local commands assume that you have the following repositories checked out in parent dir
#   ..
#   ../docker-elasticsearch  
#   ../docker-postgresql
#   ../docker-ubuntu-base
#   ../globallometree
#

install-utilities: add-postgres-repo apt-update
	sudo apt-get install -y postgresql-client-9.3 git 

apt-update:
	sudo apt-get update

apt-upgrade:
	sudo apt-get upgrade

create-pip-cache-dir:
	sudo mkdir -p /opt &&
	sudo mkdir -p /opt/cache
	sudo mkdir -p /opt/cache/pip
	sudo chown ${USER}.${USER} /opt/cache/pip

run-pip-cache:
	python -m pypicache.main  --port 8090 /opt/cache/pip

# install-docker: add-docker-repo
# 	sudo apt-get install lxc-docker

add-postgres-repo:
	echo "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main" > /tmp/pgdg.list
	sudo cp /tmp/pgdg.list /etc/apt/sources.list.d/
	wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -

# add-docker-repo:
# 	sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 36A1D7869245C8950F966E92D8576A8BA88D21E9
# 	echo "deb http://get.docker.io/ubuntu docker main" > /tmp/docker.list
# 	sudo cp /tmp/docker.list /etc/apt/sources.list.d/

build-postgresql-local:
	docker build -t postgresql_server_image ../docker-postgresql

build-elasticsearch-local:
	docker build -t elasticsearch_server_image ../docker-elasticsearch

build-web-server-local: build-web-server
	
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



