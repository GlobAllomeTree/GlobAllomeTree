#!/bin/bash

/opt/globallometree_virtualenv/bin/python /opt/globallometree_app/manage.py sync_elasticsearch rawdata
/opt/globallometree_virtualenv/bin/python /opt/globallometree_app/manage.py sync_elasticsearch wooddensity
/opt/globallometree_virtualenv/bin/python /opt/globallometree_app/manage.py sync_elasticsearch allometricequation
/opt/globallometree_virtualenv/bin/python /opt/globallometree_app/manage.py sync_elasticsearch biomassexpansionfactor