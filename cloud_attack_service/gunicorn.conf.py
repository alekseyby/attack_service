import os
import multiprocessing

bind = '0.0.0.0:8000'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
accesslog = '%s' % os.environ.get('GUNICORN_ACCESS_PATH', '/opt/django/logs/gunicorn.access.log')
errorlog = '%s' % os.environ.get('GUNICORN_ERROR_PATH', '/opt/django/logs/gunicorn.errors.log')
loglevel = "warning"
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 300
# for non blocking work (https://pythonspeed.com/articles/gunicorn-in-docker/)
worker_tmp_dir = "/dev/shm"
keepalive = 100
