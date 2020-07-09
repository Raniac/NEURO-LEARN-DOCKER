FROM raniac/neuro-learn-docker:base
MAINTAINER raniac <leibingye@outlook.com>

WORKDIR /neuro-learn
ADD . /neuro-learn/

RUN cp -f /neuro-learn/nginx.conf /etc/nginx

CMD ["sh","/neuro-learn/start.sh"]
