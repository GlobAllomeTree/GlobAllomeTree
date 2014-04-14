WEB_TAG_NAME ?= tomgruner/globallometree-web
WEB_CONTAINER_NAME ?= web
WEB_SERVER_PORT ?= 8082
WEB_SERVER_PORT_DEBUG ?= 8083
SECRET_KEY ?= top_secret 


WEB_BASE_PATH := $(abspath $(lastword $(MAKEFILE_LIST)))
WEB_BASE_DIR := $(abspath $(patsubst %/,%,$(dir $(WEB_BASE_PATH))))


#This will get evaluated when used below
WEB_SERVER_BASE_ENV = --link ${PSQL_SERVER_CONTAINER_NAME}:DB 
WEB_SERVER_BASE_ENV += --link ${ELASTIC_CONTAINER_NAME}:ES
WEB_SERVER_BASE_ENV += --link ${REDIS_CONTAINER_NAME}:REDIS  
WEB_SERVER_BASE_ENV += -v ${WEB_BASE_DIR}:/opt/code 
WEB_SERVER_BASE_ENV += -e SECRET_KEY=${SECRET_KEY}  
WEB_SERVER_BASE_ENV += -e POSTGRESQL_USER=${POSTGRESQL_USER} 
WEB_SERVER_BASE_ENV += -e POSTGRESQL_PASS=${POSTGRESQL_PASS} 
WEB_SERVER_BASE_ENV += -e POSTGRESQL_DB=${POSTGRESQL_DB} 


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
	docker run -d --name ${WEB_CONTAINER_NAME} -p ${WEB_SERVER_PORT}:80 ${WEB_SERVER_BASE_ENV} ${WEB_TAG_NAME}

web-attach:
	#Use lxc attach to attch to the webserver
	$(MAKE) dock-attach CONTAINER=${WEB_CONTAINER_NAME}

web-commit:
	docker commit -m "commit from modified web server" ${WEB_CONTAINER_NAME} ${WEB_TAG_NAME} 


####################################### WEB DEBUG #####################################


web-debug-stop:
	-@docker stop ${WEB_CONTAINER_NAME}_debug 2>/dev/null || true

web-debug-clean: web-debug-stop
	-@docker rm ${WEB_CONTAINER_NAME}_debug 2>/dev/null || true

web-debug-run: web-debug-clean
	#Run a debug server on port 8083
	docker run -i -t --name ${WEB_CONTAINER_NAME}_debug -p ${WEB_SERVER_PORT_DEBUG}:8083 -e WEB_SERVER_PORT_DEBUG=${WEB_SERVER_PORT_DEBUG} ${WEB_SERVER_BASE_ENV} ${WEB_TAG_NAME} bash /opt/code/server/startup_bash.sh

web-commit-from-debug:
	docker commit -m "commit from debug server" ${WEB_CONTAINER_NAME}_debug ${WEB_TAG_NAME} 


######################################### CELERY ####################################

celery-run: celery-clean
	#Run celery using the web container
	docker run -d --name ${WEB_CONTAINER_NAME}_celery ${WEB_SERVER_BASE_ENV} ${WEB_TAG_NAME} bash /opt/code/server/startup_celery.sh

celery-stop:
	-@docker stop ${WEB_CONTAINER_NAME}_celery 2>/dev/null || true

celery-clean:
	-@docker rm ${WEB_CONTAINER_NAME}_celery 2>/dev/null || true

####################################### DJANGO SPECIFIC #####################################

django-manage:
	# --rm will remove the container once the process finishes
	docker run -i -t --rm ${WEB_SERVER_BASE_ENV} -e COMMAND="${COMMAND}" ${WEB_TAG_NAME} bash /opt/code/server/startup_manage.sh


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


