# Resource Server

## Initiate Container

```bash
$ docker run --name service-rscs -v /home/bennyray/Projects/neuro-learn/docker/utils/ResourceServer:/rscs/files -v /opt/nls/rscs/log:/rscs/log -p 7140:80 -it --rm raniac/neuro-learn-service:rscs
```

## Build Container

```bash
$ docker build -t raniac/neuro-learn-service:rscs .
```