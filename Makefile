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






