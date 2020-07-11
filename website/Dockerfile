FROM nginx:stable

ADD . /nlw/

RUN cp -f /nlw/nginx.conf /etc/nginx/

CMD ["sh","/nlw/start.sh"]
