FROM tomgruner/globallometree-base-web

MAINTAINER Thomas Gruner "tom.gruner@gmail.com"

# install our code
# add from repository root
ADD . /opt/code/ 

# install pip requirements
RUN pip install -vr /opt/code/server/requirements.txt --allow-external pyPdf --allow-unverified pyPdf

# remove local settings if there was a dev version and instead use the server version
RUN rm -f /opt/code/globallometree/settings_local.py
RUN cp /opt/code/globallometree/settings_local.py.server  /opt/code/globallometree/settings_local.py