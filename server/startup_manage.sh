#!/bin/bash
python /home/docker/code/server/save_env.py

LOCAL_SETTINGS_FILE=/home/docker/code/globallometree/settings_local.py

if [ ! -f $LOCAL_SETTINGS_FILE ];
then
   echo "Copying settings_local.py.server to settings_local.py"
   cp /home/docker/code/globallometree/settings_local.py.server /home/docker/code/globallometree/settings_local.py
fi

cd /home/docker/code

./manage.py ${COMMAND}