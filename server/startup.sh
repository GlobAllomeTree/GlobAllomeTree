#!/bin/sh
python /home/docker/code/server/save_env.py
/home/docker/code/globallometree/manage.py collectstatic --noinput
supervisord -n