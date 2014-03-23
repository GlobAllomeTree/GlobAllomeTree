#!/bin/bash
python /home/docker/code/server/save_env.py

#Add a reference to our upstream elastic search so nginx can reference it
cat << EOF > /etc/nginx/elasticsearch_upstream.conf
upstream elasticsearch_upstream  {
  server $ES_PORT_9200_TCP_ADDR:$ES_PORT_9200_TCP_PORT;
}
EOF

supervisord -n