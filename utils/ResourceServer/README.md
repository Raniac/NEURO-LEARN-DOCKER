# Resource Server

## Initiate Container

```bash
$ docker run --name service-rscs -v /data:/rscs/files -v /opt/nls/rscs/log:/rscs/log -p 7140:80 -d raniac/resource-server:dev
```

## Build Container

```bash
$ docker build -t raniac/resource-server:dev .
```