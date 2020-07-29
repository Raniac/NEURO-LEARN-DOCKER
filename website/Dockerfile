FROM nginx:stable

ADD nginx.conf /nlw/
ADD frontend/dist /nlw/dist

RUN cp -f /nlw/nginx.conf /etc/nginx/
RUN mkdir /etc/nginx/html/
RUN mkdir /nlw/log/
RUN cp -f /nlw/dist/index.html /etc/nginx/html/
