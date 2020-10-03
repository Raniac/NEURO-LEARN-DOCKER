cd /nls-sa/app;
export C_FORCE_ROOT=true;
export LC_ALL=C.UTF-8;
export LANG=C.UTF-8;
nohup uvicorn main:app --host '0.0.0.0' --port 7410 --log-level debug >> /nls-sa/log/uvicorn.access.log &
celery worker -A main.celery -l info -f /nls-sa/log/celery.log
