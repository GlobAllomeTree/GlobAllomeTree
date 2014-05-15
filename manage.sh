#/bin/bash

#This is used to run manage.py using the docker container as context

#Get the directory of this file
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#This command shares the hosts code directory with the container
#to allow for dev
docker run -i -t \
	-v ${DIR}:/opt/code \
	-v /opt/data/web:/opt/data \
	-p 8083:8083 \
	--net="host" \
	tomgruner/globallometree-web \
	/opt/code/manage.py $1