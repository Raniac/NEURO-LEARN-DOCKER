cd /nls-sgn/app;
export C_FORCE_ROOT=true;
nohup celery worker -A main.celery --loglevel=info >> /nls-sgn/log/celery.log &
nohup gunicorn main:app --bind 0.0.0.0:7014 --workers 4 --log-level debug >> /nls-sgn/log/gunicorn.log &