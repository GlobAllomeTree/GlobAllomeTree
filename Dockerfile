from ubuntu_base

MAINTAINER GlobAllomeTree "globallometree@fao.org"

run apt-get install -y nginx

# install uwsgi now because it takes a little while
run pip install uwsgi==2.0

# install nginx
run add-apt-repository -y ppa:nginx/stable

# install mysql client so that django doesn't complain
run apt-get install -y python-mysqldb
run apt-get -y install mysql-client

# install our code
# add from repository root
add . /home/docker/code/ 

# setup all the configfiles
run echo "daemon off;" >> /etc/nginx/nginx.conf
run rm /etc/nginx/sites-enabled/default
run ln -s /home/docker/code/server/nginx.conf /etc/nginx/sites-enabled/
run ln -s /home/docker/code/server/supervisor.conf /etc/supervisor/conf.d/

# run pip install
# pydot has insecure external files at this time, and newer versions of pip require the exception
run pip install -r /home/docker/code/requirements.pip --allow-external pydot --allow-unverified pydot

# create a few folders  (after Joe removes from repo)
# run mkdir /home/docker/code/irmis/static
# run mkdir /home/docker/code/irmis/media

# set local settings
run cp /home/docker/code/irmis/settings_local.py.sample  /home/docker/code/irmis/settings_local.py

expose 8081
expose 8082

CMD ["/bin/bash", "/home/docker/code/server/startup.sh"]