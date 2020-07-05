service nginx start;
service redis-server start;
cd /nld_sgn/app;
nohup celery worker -A main.celery --loglevel=info >> celery.log &
gunicorn main:app --bind 0.0.0.0:8000 --workers 4 --log-level debug;