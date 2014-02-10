TAG="postgresql_server"

CONTAINER_ID=$(docker ps | grep $TAG | awk '{print $1}')

IP=$(docker inspect $CONTAINER_ID | python -c 'import json,sys;obj=json.load(sys.stdin);print obj[0]["NetworkSettings"]["IPAddress"]')
#echo "DROP DATABASE IF EXISTS irmis;" | mysql -h $IP -u root  
#echo "CREATE DATABASE irmis;" | mysql -h $IP -u root  
#echo "irmis database created, now importing"

gunzip /home/vagrant/synced/globallometree.import.sql.gz  
psql -h $IP -U globallometree < /home/vagrant/synced/globallometree.import.sql