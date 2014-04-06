#!/bin/bash
python /opt/code/server/save_env.py

cd /opt/code 
C_FORCE_ROOT=true celery -A globallometree worker -l info