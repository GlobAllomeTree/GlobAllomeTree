#!/bin/bash
python /opt/code/server/save_env.py

LOCAL_SETTINGS_FILE=/opt/code/globallometree/settings_local.py

if [ ! -f $LOCAL_SETTINGS_FILE ];
then
   echo "Copying settings_local.py.server to settings_local.py"
   cp /opt/code/globallometree/settings_local.py.server /opt/code/globallometree/settings_local.py
else
   echo ""
   echo ""
   echo "Warning, local_settings.py already exists. Make sure that any changes in settings_local.py.server have been copied over if required"
   echo ""	
fi

cd /opt/code

echo ""
echo "Tour friendly django debug server"
echo ""
echo "Run Debug Server "
echo "./manage.py runserver 0.0.0.0:${WEB_SERVER_PORT_DEBUG}" 
echo " - then open your browser to http://127.0.0.1:${WEB_SERVER_PORT_DEBUG}/"
echo ""
echo "iPython Shell "
echo "./manage.py shell_plus" 
echo ""
echo ""
echo "Rebuild Elasticsearch Index"
echo "./manage.py rebuild_index" 
echo ""

/bin/bash

echo ""
echo "Nice to see you and have a great day!!"
echo ""