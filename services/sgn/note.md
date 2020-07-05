# Dev Note

## Development

### Build a Docker image of Ubuntu with Python and Flask

```Dockerfile
FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y python3 \
                        python3-dev \
                        python3-pip \
    && apt-get clean \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/*

RUN export LC_ALL=C.UTF-8 \
    && export LANG=C.UTF-8

RUN pip3 install Flask -i https://pypi.doubanio.com/simple

CMD ["/bin/bash"]
```

```bash
$ docker build -t ubuntu-with-python:dev .
```

### Create and Update the Docker image of Dev Env

#### Create

```Dockerfile
FROM ubuntu-with-python:dev

RUN apt-get update \
    && apt-get install redis-server

RUN pip3 install -r requirements.txt -i https://pypi.doubanio.com/simple

CMD ["/bin/bash"]
```

```bash
$ docker build -t nld-sgn-env:dev .
```

#### Update

```bash
$ docker ps
CONTAINER ID        IMAGE                            COMMAND             CREATED             STATUS              PORTS                    NAMES
9c1f1d3e7927        nld-sgn-env:dev   "/bin/bash"         8 minutes ago       Up 8 minutes                            pensive_hofstadter
$ docker commit 9c1f1d3e7927 nld-sgn-env:dev
```

### Build Dev Env Docker from imcomking/pytorch_geometric:latest

```Dockerfile
FROM imcomking/pytorch_geometric:latest

RUN apt-get update \
    && apt-get -y install nginx \
    && apt-get -y install redis-server \
    && apt-get clean \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/*

ADD . /workspace/

RUN pip install -r requirements.txt -i https://pypi.doubanio.com/simple

CMD ["/bin/bash"]
```

```bash
$ cd env/nld-sgn-env/
$ docker build -t nld-sgn-env:pg .
```

### Initiate Dev Env Container

```bash
$ docker run -it --rm -v /c/Users/Benny/Documents/Projects/nld_sgn:/nld_sgn -p 80:80 nld-sgn-env:pg /bin/bash
$ # service nginx start
$ service redis-server start
$ cd /nld_sgn/app
$ nohup celery worker -A main.celery --loglevel=info >> celery.log &
$ python main.py
$ # gunicorn main:app --bind 0.0.0.0:8000 --workers 4 --log-level debug
```

## Deployment

### Build Docker Registry for Kubernetes

#### Server End

```bash
$ docker search registry
$ docker run -d -p 5000:5000 -v /docker/registry/data:/var/lib/registry --privileged=true --restart=always --name registry registry:latest
```

> Note that the port 5000 of the server need to be opened.

#### User End

- Ubuntu: configure ```"insecure-registries"``` in ```/etc/docker/daemon.json```;
- Windows: configure ```"insecure-registries"``` in Daemon of Docker Desktop.

```bash
$ docker tag ubuntu-with-python:dev 120.79.49.129:5000/ubuntu-with-python:latest
$ docker push 120.79.49.129:5000/ubuntu-with-python
```

### Build NEURO-LEARNN-DOCKER-SGN with Dev Env Docker

```Dockerfile
FROM nld-sgn-env:pg

ADD . /nld_sgn/

CMD ["sh","/nld_sgn/start.sh"]
```

> Use .dockerignore to neglect useless files.

### Initiate NLD-SGN container

- Mount host directories into container in order to add writable files, such as new models.
```bash
$ docker run -it --rm -v /path/to/models:/nld_sgn/models -p 80:80 raniac/neuro-learn-docker:sgn
```
- Or use docker-compose.

### Use Docker-Compose to Deploy Containerized Services

```yml
version: '2'

services:
  sgn-service:
    image: 120.79.49.129:5000/neuro-learn-docker:sgn
    restart: on-failure
    hostname: sgn-server
    ports:
      - "80:80"
    volumes:
      - /c/Users/Benny/Documents/Projects/nld_sgn/models:/nld_sgn/models
    # environment:
    #   KAFKA_ADVERTISED_HOST_NAME: localhost
    # depends_on:
    #   - zoo1
    container_name: sgn-service
```

## References

- [Train and Deploy Machine Learning Model With Web Interface - PyTorch & Flask](https://imadelhanafi.com/posts/train_deploy_ml_model/)
- [Flask Documentation](https://dormousehole.readthedocs.io/en/latest/)
- [在服务器的docker中部署深度学习模型（flask框架）](https://blog.csdn.net/MissShihong/article/details/103313396)
- [关于docker-Compose基本使用](https://www.jianshu.com/p/808385b9e4aa)
- [Flask 应用如何部署](https://www.cnblogs.com/hellohorld/p/10033720.html)
- [Docker+K8S笔记(二)：Linux安装docker-registry](https://my.oschina.net/u/4075242/blog/3068384)

## Appendix

### Nginx Configuration

See nginx.conf.

### Docker-Compose Configuration

See docker-compose.yml.
