cd /nls-ml/app;
export C_FORCE_ROOT=true;
nohup celery worker -A main.celery --loglevel=info >> celery.log &
gunicorn main:app --bind 0.0.0.0:4701 --workers 4 --log-level debug;
