service nginx start;
service rabbitmq-server start;
cd /neuro-learn/app/;
uwsgi -d uwsgi.log uwsgi.ini;
export C_FORCE_ROOT='True';
python3.6 manage.py celeryd -l info;
