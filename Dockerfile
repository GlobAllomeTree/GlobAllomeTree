from ubuntu_base

MAINTAINER GlobAllomeTree "globallometree@fao.org"

# install uwsgi now because it takes a little while
RUN pip install uwsgi==2.0

# install nginx
RUN LC_ALL=en_US.UTF-8 DEBIAN_FRONTEND=noninteractive apt-get install -y nginx

# install postgresql support for python / django 
RUN LC_ALL=en_US.UTF-8 DEBIAN_FRONTEND=noninteractive  apt-get install -y python-psycopg2

# install python imaging requirements 
RUN LC_ALL=en_US.UTF-8 DEBIAN_FRONTEND=noninteractive  apt-get install -y libjpeg62-dev zlib1g-dev libfreetype6-dev liblcms1-dev

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