FROM tomgruner/docker-base

MAINTAINER Thomas Gruner "tom.gruner@gmail.com"

RUN apt-get install -y libxml2-dev libxslt1-dev python-lxml
RUN apt-get install -y libtiff4-dev libjpeg62-dev zlib1g-dev \
    libfreetype6-dev tcl8.5-dev tk8.5-dev python-tk
#Install the requirements first to keep image changes as minimal as possible
#This takes advantage of the caching mechanism
#By adding the requirement files before the code, they only invalidate the cache
#if they have changed
ADD ./server/requirements.compiled.txt  /tmp/reqs/requirements.compiled.txt
RUN pip install -vr /tmp/reqs/requirements.compiledtxt 
ADD ./server/requirements.txt  /tmp/reqs/requirements.txt
RUN pip install -vr /tmp/reqs/requirements.txt --allow-external pyPdf --allow-unverified pyPdf

# install our code
# add from repository root
# This happens last since it generally always invalidate
ADD . /opt/code/ 

# remove local settings if there was a dev version and instead use the server version
RUN rm -f /opt/code/globallometree/settings_local.py
RUN cp /opt/code/globallometree/settings_local.server.py  /opt/code/globallometree/settings_local.py