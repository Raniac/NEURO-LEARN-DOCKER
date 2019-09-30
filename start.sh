service nginx start;
service rabbitmq-server start;
cd /neuro-learn/app/;
nohup uwsgi --ini uwsgi.ini >> uwsgi.log &;
export C_FORCE_ROOT='True';
python3.6 manage.py celeryd -l info;
