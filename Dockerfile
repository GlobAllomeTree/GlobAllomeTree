FROM tomgruner/docker-base

MAINTAINER Thomas Gruner "tom.gruner@gmail.com"

#Install the requirements first to keep image changes as minimal as possible
#This takes advantage of the caching mechanism
ADD ./server/requirements.txt  /tmp/requirements.txt
RUN pip install -vr /tmp/requirements.txt --allow-external pyPdf --allow-unverified pyPdf

RUN mkdir -p /opt/logs/

# install our code
# add from repository root
ADD . /opt/code/ 

# remove local settings if there was a dev version and instead use the server version
RUN rm -f /opt/code/globallometree/settings_local.py
RUN cp /opt/code/globallometree/settings_local.py.server  /opt/code/globallometree/settings_local.py