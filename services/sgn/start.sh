# TODO see if service can be called through port 7014 without nginx
# service nginx start;
service redis-server start;
cd /nld_sgn/app;
nohup celery worker -A main.celery --loglevel=info >> celery.log &
gunicorn main:app --bind 0.0.0.0:7014 --workers 4 --log-level debug;