## ======== BUILD IMAGES ========

# docker build -t raniac/neuro-learn-env:api ../envs/api/;
# docker build -t raniac/neuro-learn-env:ml ../envs/ml/;
# docker build -t raniac/neuro-learn-env:sa ../envs/sa/;
# docker build -t raniac/neuro-learn-env:sgn ../envs/sgn/;

# docker build -t raniac/neuro-learn-website:dev ../website/;
# docker build -t raniac/neuro-learn-service:api ../services/api/;
# docker build -t raniac/neuro-learn-service:ml ../services/ml/;
# docker build -t raniac/neuro-learn-service:sa ../services/sa/;
# docker build -t raniac/neuro-learn-service:sgn ../services/sgn/;

## ======== PULL IMAGES ========

# docker pull raniac/neuro-learn-website:dev;
# docker pull raniac/neuro-learn-service:api;
# docker pull raniac/neuro-learn-service:ml;
# docker pull raniac/neuro-learn-service:sa;
# docker pull raniac/neuro-learn-service:sgn;

# docker pull raniac/neuro-learn-env:api;
# docker pull raniac/neuro-learn-env:ml;
# docker pull raniac/neuro-learn-env:sa;
# docker pull raniac/neuro-learn-env:sgn;

## ======== INITIATE CONTAINERS FOR DEV ========

# docker run -it --rm --network host -v /home/raniac/dev/NEURO-LEARN-DOCKER/services/api:/nls-api raniac/neuro-learn-service:api /bin/bash
# docker run -it --rm --network host -v /home/raniac/dev/NEURO-LEARN-DOCKER/services/ml:/nls-ml raniac/neuro-learn-service:ml /bin/bash
# docker run -it --rm --network host -v /home/raniac/dev/NEURO-LEARN-DOCKER/services/sa:/nls-sa raniac/neuro-learn-service:sa /bin/bash
# docker run -it --rm --network host -v /home/raniac/dev/NEURO-LEARN-DOCKER/services/sgn:/nls-sgn raniac/neuro-learn-service:sgn /bin/bash

## ======== REMOVE IMAGES WITHOUT TAGS ========

# docker images | grep none | awk '{print $3}' | xargs docker rmi

## ======== VIEW SERVICE LOGS ========

# sudo tail -n 100 /opt/nls/api/log/uwsgi.log
# sudo tail -n 100 /opt/nls/ml/log/celery.log
# sudo tail -n 100 /opt/nls/ml/log/gunicorn.error.log
# sudo tail -n 100 /opt/nls/ml/log/gunicorn.access.log

## ======== BUILD WEBSITE ========

# cnpm run build
# cp -r dist/* ../../../website/
