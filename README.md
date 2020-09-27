![logo](doc/logo.png)

# NEURO-LEARN-DOCKER

**Before you start, feel free to read our [article](https://www.jianshu.com/p/06f0451463fe) about NLD! :-)**

## Quick Start

> 中文使用文档详见[Getting Started with NEURO-LEARN](https://www.jianshu.com/p/067747c881ee).

### Fast Deployment

```bash
# In the case of standalone deployment, the following ips are the same
# which is the ip of the deployed host
root@machine:/$ echo "{host ip for ml-service} ml.neurolearn.com" >> /etc/hosts
root@machine:/$ echo "{host ip for sgn-service} sgn.neurolearn.com" >> /etc/hosts
root@machine:/$ echo "{host ip for db-server} db.neurolearn.com" >> /etc/hosts
root@machine:/$ echo "{host ip for hdfs-master} hdfs.neurolearn.com" >> /etc/hosts
# Open a terminal on the host, change directory to NEURO-LEARN-DOCKER/utils
user@machine:~/NEURO-LEARN-DOCKER/utils$ docker-compose up -d
# To stop the containers
user@machine:~/NEURO-LEARN-DOCKER/utils$ docker-compose down
```

> NOTE that NEURO-LEARN-DOCKER requires a deployed MySQL database server with corresponding tables.
> Starting fresh, one needs to follow the instructions mentioned in [wiki](https://github.com/Raniac/NEURO-LEARN-DOCKER/wiki) to initiate the database.

### Client Configuration

```bash
# Configure the ip for api-service apis
root@machine:/$ echo "120.79.49.129 api.neurolearn.com" >> /etc/hosts
# Remember to configure the security options to allow insecure mixed contents
# Now open a browser and type the address https://raniac.github.io/neuro-learn-website/
# VOILA!
```

## NLD Microservices Framework

![framework](doc/framework.png)

## NLD Continuous Integration

![continuous_integration](doc/continuous_integration.png)

## NLD Website UI

> 中文文档详见[Getting Started with NEURO-LEARN](https://www.jianshu.com/p/067747c881ee)。

### Home

![home](doc/screenshots/home.png)

### Login

![login](doc/screenshots/login.png)

### Profile

![profile](doc/screenshots/profile.png)

### Projects Overview

![projects-overview](doc/screenshots/projects-overview.png)

### Projects Data

![projects-data](doc/screenshots/projects-data.png)

### New Projects

![new-project](doc/screenshots/new-project.png)

### New ML Task

![new-ml-task](doc/screenshots/new-ml-task.png)

### New DL Task

![new-dl-task](doc/screenshots/new-dl-task.png)

### Analysis Overview

![analysis-overview](doc/screenshots/analysis-overview.png)

### Analysis Submissions

![analysis-submissions](doc/screenshots/analysis-submissions.png)

### Analysis Viewer

![analysis-viewer](doc/screenshots/analysis-viewer.png)
