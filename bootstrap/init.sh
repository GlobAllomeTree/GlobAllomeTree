pip install -r bootstrap/requirements.txt
./manage.py syncdb
./manage.py loaddata bootstrap/fixtures/Country.json
./manage.py loaddata bootstrap/fixtures/TreeEquation.json 
./manage.py loaddata bootstrap/fixtures/users.json 
