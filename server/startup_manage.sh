#!/bin/bash
python /opt/code/server/save_env.py

LOCAL_SETTINGS_FILE=/opt/code/globallometree/settings_local.py

if [ ! -f $LOCAL_SETTINGS_FILE ];
then
   echo "Copying settings_local.py.server to settings_local.py"
   cp /opt/code/globallometree/settings_local.py.server /opt/code/globallometree/settings_local.py
fi

cd /opt/code

./manage.py ${COMMAND}