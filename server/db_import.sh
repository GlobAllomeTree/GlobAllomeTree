TAG="postgresql_server"

CONTAINER_ID=$(docker ps | grep $TAG | awk '{print $1}')

IP=$(docker inspect $CONTAINER_ID | python -c 'import json,sys;obj=json.load(sys.stdin);print obj[0]["NetworkSettings"]["IPAddress"]')

gunzip /home/vagrant/synced/globallometree.import.sql.gz  
psql -h $IP -U globallometree < /home/vagrant/synced/globallometree.import.sql