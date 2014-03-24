WEB_TAG_NAME ?= tomgruner/globallometree-web
WEB_CONTAINER_NAME ?= web

WEB_BASE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
WEB_BASE_DIR := $(abspath $(patsubst %/,%,$(dir $(WEB_BASE_PATH))))

#This will get evaluated when used below
WEB_SERVER_BASE_ENV = --link postgresql_server:DB --link elasticsearch:ES -v ${WEB_BASE_DIR}:/home/docker/code -e SECRET_KEY=${SECRET_KEY}  -e POSTGRESQL_USER=${POSTGRESQL_USER} -e POSTGRESQL_PASS=${POSTGRESQL_PASS} -e POSTGRESQL_DB=${POSTGRESQL_DB} 


####################################### WEB SERVER #####################################


#All names should be prefixed with web
web-stop:
	-@docker stop ${WEB_CONTAINER_NAME} 2>/dev/null || true


web-clean: web-stop
	-@docker rm ${WEB_CONTAINER_NAME} 2>/dev/null || true


web-build:
	cd ${WEB_BASE_DIR} && docker build -t ${WEB_TAG_NAME} .


web-run: web-clean
	#Run the webserver on port 8082
	docker run -d --name web_server -p ${WEB_SERVER_PORT}:80 ${WEB_SERVER_BASE_ENV} ${WEB_TAG_NAME}



####################################### WEB DEBUG #####################################


web-run-debug:
	#Run a debug server on port 8083
	-@docker stop web_server_debug 2>/dev/null || true
	-@docker rm web_server_debug 2>/dev/null || true
	docker run -i -t --name web_server_debug -p 8083:8083 ${WEB_SERVER_BASE_ENV} ${WEB_TAG_NAME} bash /home/docker/code/server/startup_bash.sh

web-attach:
	#Use lxc attach to attch to the webserver
	$(MAKE) dock-attach CONTAINER=${WEB_CONTAINER_NAME}


####################################### DJANGO SPECIFIC #####################################

django-manage:
	#Run manage.py 
	#Example)  django-manage COMMAND="collectstatic --noinput"
	-@docker stop django_manage 2>/dev/null || true
	-@docker rm django_manage 2>/dev/null || true
	docker run -i -t --name django_manage ${WEB_SERVER_BASE_ENV} -e COMMAND="${COMMAND}" web_server_image bash /home/docker/code/server/startup_manage.sh


django-collectstatic:
	$(MAKE) django-manage COMMAND="collectstatic --noinput"

django-rebuild-index:
	$(MAKE) django-manage COMMAND="rebuild_index --noinput"


####################################### MODEL GRAPHING #####################################

graph-all-models:
	$(MAKE) django-manage COMMAND="graph_models -a -o all_models.png"

graph-data-models:
	$(MAKE) django-manage COMMAND="graph_models taxonomy allometric_equations wood_densities locations common -x modified,created -o data_models_phase_2.png"

graph-p1-data-models:
	$(MAKE) django-manage COMMAND="graph_models data -o data_models_phase_1.png"








