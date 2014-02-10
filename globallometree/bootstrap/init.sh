pip install -r bootstrap/requirements.txt
./manage.py syncdb
./manage.py loaddata fixtures/data.json