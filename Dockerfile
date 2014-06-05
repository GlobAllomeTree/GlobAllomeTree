FROM tomgruner/docker-base

MAINTAINER Thomas Gruner "tom.gruner@gmail.com"

#Install the requirements first to keep image changes as minimal as possible
#This takes advantage of the caching mechanism
ADD ./server  /tmp/reqs/
RUN pip install -vr /tmp/reqs/requirements.core.txt
RUN pip install -vr /tmp/reqs/requirements.pdf.txt --allow-external pyPdf --allow-unverified pyPdf
RUN pip install -vr /tmp/reqs/requirements.elasticsearch.txt
RUN pip install -vr /tmp/reqs/requirements.cms.txt
RUN pip install -vr /tmp/reqs/requirements.txt

# install our code
# add from repository root
ADD . /opt/code/ 

# remove local settings if there was a dev version and instead use the server version
RUN rm -f /opt/code/globallometree/settings_local.py
RUN cp /opt/code/globallometree/settings_local.server.py  /opt/code/globallometree/settings_local.py