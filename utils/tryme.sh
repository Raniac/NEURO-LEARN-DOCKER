## !!!! BUILD IMAGES !!!!

# docker build -t raniac/neuro-learn-env:commons ../envs/commons/;
# docker build -t raniac/neuro-learn-env:ml ../envs/ml/;
# docker build -t raniac/neuro-learn-env:sgn ../envs/sgn/;

# docker build -t raniac/neuro-learn-website:dev ../website/;
docker build -t raniac/neuro-learn-service:commons ../services/commons/;
docker build -t raniac/neuro-learn-service:ml ../services/ml/;
docker build -t raniac/neuro-learn-service:sgn ../services/sgn/;

## !!!! PUSH IMAGES !!!!

# docker push raniac/neuro-learn-website:dev;
# docker push raniac/neuro-learn-service:commons;
# docker push raniac/neuro-learn-service:ml;
# docker push raniac/neuro-learn-service:sgn;

# docker push raniac/neuro-learn-env:commons;
# docker push raniac/neuro-learn-env:ml;
# docker push raniac/neuro-learn-env:sgn;

## !!!! INITIATE CONTAINERS FOR DEV !!!!

# docker run -it --rm --network host -v /home/raniac/dev/NEURO-LEARN-DOCKER/services/commons:/nls-commons neuro-learn-service:commons /bin/bash
# docker run -it --rm --network host -v /home/raniac/dev/NEURO-LEARN-DOCKER/services/ml:/nls-ml neuro-learn-service:ml /bin/bash
# docker run -it --rm --network host -v /home/raniac/dev/NEURO-LEARN-DOCKER/services/sgn:/nls-sgn neuro-learn-service:sgn /bin/bash