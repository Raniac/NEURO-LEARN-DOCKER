FROM nginx:stable

ADD . /nlw/

RUN cp -f /nlw/nginx.conf /etc/nginx/
RUN mkdir /etc/nginx/html/
RUN cp -f /nlw/dist/index.html /etc/nginx/html/
