FROM tomgruner/globallometree-base

MAINTAINER Thomas Gruner "tom.gruner@gmail.com"

ENV LC_ALL en_US.UTF-8
ENV DEBIAN_FRONTEND noninteractive 

# install uwsgi now because it takes a little while
RUN pip install uwsgi==2.0

# install postgresql support for python / django 
RUN apt-get install -y libpq-dev postgresql-client

# install python imaging requirements and shell plus reqs 
# graphviz graphviz-dev pkg-config added for shell plus graph models 
# ipython-notebook added for shell plus ipython
RUN apt-get install -y  libjpeg62-dev zlib1g-dev libfreetype6-dev liblcms1-dev graphviz graphviz-dev pkg-config ipython-notebook

#Create the /opt/code and /opt/run directories
RUN mkdir -p /opt/code && mkdir -p /opt/logs && && mkdir -p /opt/run

# install our code
# add from repository root
ADD . /opt/code/ 

# install pip requirements
RUN pip install -vr /opt/code/server/requirements.txt --allow-external pyPdf --allow-unverified pyPdf

# set local settings
RUN cp /opt/code/globallometree/settings_local.py.server  /opt/code/globallometree/settings_local.py

