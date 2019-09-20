FROM neuro-learn-docker:dev
MAINTAINER raniac <leibingye@outlook.com>

WORKDIR /neuro-learn
ADD . /neuro-learn/

RUN cp -f /neuro-learn/nginx.conf /etc/nginx

CMD ["/bin/bash"]
