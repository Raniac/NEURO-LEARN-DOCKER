# Resource Server

## Initiate Container

```bash
$ docker run --name service-rscs -v /data:/rscs/files -v /opt/nls/rscs/log:/rscs/log -p 7140:80 -d raniac/neuro-learn-service:rscs
```

## Build Container

```bash
$ docker build -t raniac/neuro-learn-service:rscs .
```