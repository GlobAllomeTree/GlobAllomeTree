FROM tomgruner/globallometree-base

MAINTAINER Thomas Gruner "tom.gruner@gmail.com"

RUN mkdir -p /home && mkdir -p /opt && mkdir -p /opt/run && mkdir -p /opt/logs

ENV BUILD 1
ENV LC_ALL en_US.UTF-8

#USE LOCAL CACHE
#REQUIRES docker-proxy to be running on ports 8095 for pypi and 8096 for apt-cacher-ng
#Setup Proxies (Comment Out the following lines if your proxy is not set up)
#TODO: Make a clearer error message when proxy is not running
#apt-cacher-ng
# RUN /sbin/ip route | awk '/default/ { print "Acquire::http::Proxy \"http://"$3":8096\";" }' > /etc/apt/apt.conf.d/30proxy
# #pypi
# ENV PIP_CONFIG_FILE /opt/pip.conf
# RUN echo "[global]" > /opt/pip.conf
# RUN /sbin/ip route | awk '/default/ { print "index-url = http://"$3":8095/simple" }' >> /opt/pip.conf
# RUN cat /opt/pip.conf

# install uwsgi now because it takes a little while
RUN pip install uwsgi==2.0

# install nginx
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y nginx

# install postgresql support for python / django 
RUN DEBIAN_FRONTEND=noninteractive  apt-get install -y libpq-dev postgresql-client

# install python imaging requirements and shell plus reqs 
# graphviz graphviz-dev pkg-config added for shell plus graph models 
# ipython-notebook added for shell plus ipython
RUN DEBIAN_FRONTEND=noninteractive  apt-get install -y  libjpeg62-dev zlib1g-dev libfreetype6-dev liblcms1-dev graphviz graphviz-dev pkg-config ipython-notebook

# install our code
# add from repository root
ADD . /opt/code/ 

# setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /opt/code/server/nginx.conf /etc/nginx/sites-enabled/
RUN ln -s /opt/code/server/supervisor.conf /etc/supervisor/conf.d/

# install pip requirements
RUN pip install -vr /opt/code/server/requirements.txt --allow-external pyPdf --allow-unverified pyPdf

# set local settings
RUN cp /opt/code/globallometree/settings_local.py.server  /opt/code/globallometree/settings_local.py

CMD ["/bin/bash", "/opt/code/server/startup.sh"]