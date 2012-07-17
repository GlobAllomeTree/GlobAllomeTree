Basic setup for a new project
=============================

All paths given are relative to the project root

1) Make a virtual environment for globallometree
   This step is optional but keeps your system python clean. 
   The --system-site-packages flag lets us install python-psycopg2 using yum or apt-get and have it available still in our environment
   virtualenv --system-site-packages globallometree_env

  

2) Activate the virtual environment
   source globalometree_env/bin/activate
   
3) Install the python requirements

   apt-get (or yum) install python-psycopg2

   pip install -r  ./bootstrap/requirements.txt
   
   
4) Create your user, database, and schema in postgresql (pgAdmin is a good tool)
  
5) Copy and modify ./bootstrap/settings_local.example.py to ./settings_local.py

6) From the same directory as manage.py is in, run ./bootstrap/init_db.sh