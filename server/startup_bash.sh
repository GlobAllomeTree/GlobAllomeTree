#!/bin/bash
python /home/docker/code/server/save_env.py

LOCAL_SETTINGS_FILE=/home/docker/code/globallometree/settings_local.py

if [ ! -f $LOCAL_SETTINGS_FILE ];
then
   echo "Copying settings_local.py.server to settings_local.py"
   cp /home/docker/code/globallometree/settings_local.py.server /home/docker/code/globallometree/settings_local.py
fi

cd /home/docker/code

#alias djm=/home/docker/code/manage.py
#alias go=/home/docker/code/manage.py runserver 0.0.0.0:8083

echo ""
echo ""
echo "Welcome to your friendly django debug server, here are a few commands to try out:"
echo ""
echo "Run Debug Server "
echo "./manage.py runserver 0.0.0.0:8083" 
#echo "djm runserver 0.0.0.0:8083" 
#echo "go" 
echo " - then open your browser to http://127.0.0.1:8083/"
echo ""
echo "Rebuild Elasticsearch Index"
echo "./manage.py rebuild_index" 
echo ""

/bin/bash

echo ""
echo "Nice to see you and have a great day!!"
echo ""