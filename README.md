# NEURO-LEARN-DOCKER

```bash
user@machine:~$ docker run -it --rm --network host raniac/neuro-learn-docker:test
root@machine:/# service nginx start
root@machine:/# service rabbitmq-server start
root@machine:/# cd /neuro-learn/app/
root@machine:/# uwsgi -d --ini uwsgi.ini
root@machine:/# export C_FORCE_ROOT='True'
root@machine:/# python3 manage.py celeryd -l info
```
> Open a browser and type your own IP address. VOILA!
