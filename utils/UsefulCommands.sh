## !!!! BUILD IMAGES !!!!

# docker build -t raniac/neuro-learn-env:api ../envs/api/;
# docker build -t raniac/neuro-learn-env:ml ../envs/ml/;
# docker build -t raniac/neuro-learn-env:sgn ../envs/sgn/;

# docker build -t raniac/neuro-learn-website:dev ../website/;
# docker build -t raniac/neuro-learn-service:api ../services/api/;
# docker build -t raniac/neuro-learn-service:ml ../services/ml/;
# docker build -t raniac/neuro-learn-service:sgn ../services/sgn/;

## !!!! PUSH IMAGES !!!!

# docker push raniac/neuro-learn-website:dev;
# docker push raniac/neuro-learn-service:api;
# docker push raniac/neuro-learn-service:ml;
# docker push raniac/neuro-learn-service:sgn;

# docker push raniac/neuro-learn-env:api;
# docker push raniac/neuro-learn-env:ml;
# docker push raniac/neuro-learn-env:sgn;

## !!!! INITIATE CONTAINERS FOR DEV !!!!

# docker run -it --rm --network host -v /home/raniac/dev/NEURO-LEARN-DOCKER/services/api:/nls-api raniac/neuro-learn-service:api /bin/bash
# docker run -it --rm --network host -v /home/raniac/dev/NEURO-LEARN-DOCKER/services/ml:/nls-ml raniac/neuro-learn-service:ml /bin/bash
# docker run -it --rm --network host -v /home/raniac/dev/NEURO-LEARN-DOCKER/services/sgn:/nls-sgn raniac/neuro-learn-service:sgn /bin/bash

## !!!! REMOVE IMAGES WITHOUT TAGS !!!!

# docker images | grep none | awk '{print $3}' | xargs docker rmi