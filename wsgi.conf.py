bind = "unix:///tmp/globallometree.gunicorn.sock"
workers = 2
worker_class = "gevent"
user = "globallometree"
group = "globallometree"