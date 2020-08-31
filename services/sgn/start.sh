cd /nls-sgn/app;
export C_FORCE_ROOT=true;
gunicorn main:app -D --bind 0.0.0.0:7014 --workers 4 --log-level debug --access-logfile /nls-sgn/log/gunicorn.access.log --error-logfile /nls-sgn/log/gunicorn.error.log;
celery worker -A main.celery -l info -f /nls-sgn/log/celery.log
