from ubuntu_base

MAINTAINER GlobAllomeTree "globallometree@fao.org"

#REQUIRES docker-proxy to be running on ports 8095 for pypi and 8096 for apt-cacher-ng
RUN mkdir -p /home && mkdir -p /home/docker

ENV BUILD 1
ENV LC_ALL en_US.UTF-8

#Setup Proxies (Comment Out the following lines if your proxy is not set up)
#TODO: Make a clearer error message when proxy is not running
RUN /sbin/ip route | awk '/default/ { print "Acquire::http::Proxy \"http://"$3":8096\";" }' > /etc/apt/apt.conf.d/30proxy

ENV PIP_CONFIG_FILE /home/docker/pip.conf
RUN echo "[global]" > /home/docker/pip.conf
RUN /sbin/ip route | awk '/default/ { print "index-url = http://"$3":8095/simple" }' >> /home/docker/pip.conf
RUN cat /home/docker/pip.conf

# install uwsgi now because it takes a little while
RUN pip install uwsgi==2.0

# install nginx
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y nginx

# install postgresql support for python / django 
RUN DEBIAN_FRONTEND=noninteractive  apt-get install -y python-psycopg2 postgresql-client

# install python imaging requirements 
RUN DEBIAN_FRONTEND=noninteractive  apt-get install -y libjpeg62-dev zlib1g-dev libfreetype6-dev liblcms1-dev

# install our code
# add from repository root
add . /home/docker/code/ 

# setup all the configfiles
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default
RUN ln -s /home/docker/code/server/nginx.conf /etc/nginx/sites-enabled/
RUN ln -s /home/docker/code/server/supervisor.conf /etc/supervisor/conf.d/

# install pip requirements
RUN pip install -vr /home/docker/code/server/requirements.txt --allow-external PIL --allow-unverified PIL --allow-external pyPdf --allow-unverified pyPdf

# create a few folders 
# RUN mkdir /home/docker/code/static_collected

# set local settings
RUN cp /home/docker/code/globallometree/settings_local.py.server  /home/docker/code/globallometree/settings_local.py

CMD ["/bin/bash", "/home/docker/code/server/startup.sh"]