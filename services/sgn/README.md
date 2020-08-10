# NEURO-LEARN-SERVICE

## ```api```

### Start ```raniac/neuro-learn-service:api``` Container

```bash
$ docker run -it --rm --network host raniac/neuro-learn-service:api
```

### Build ```raniac/neuro-learn-service:api``` Image

```bash
$ docker build -t raniac/neuro-learn-service:api .
```

### Initiate ```raniac/neuro-learn-service:api``` Container for Dev

```bash
$ docker run -it --rm --network host -v /home/raniac/dev/NEURO-LEARN-DOCKER/services/api:/nls-api raniac/neuro-learn-service:api /bin/bash
```

## ```ml```

### Start ```raniac/neuro-learn-service:ml``` Container

```bash
$ docker run -it --rm --network host raniac/neuro-learn-service:ml
```

### Build ```raniac/neuro-learn-service:ml``` Image

```bash
$ docker build -t raniac/neuro-learn-service:ml .
```

### Initiate ```raniac/neuro-learn-service:ml``` Container for Dev

```bash
$ docker run -it --rm --network host -v /home/raniac/dev/NEURO-LEARN-DOCKER/services/ml:/nls-ml raniac/neuro-learn-service:ml /bin/bash
```

## ```sgn```

### Introduction

NEURO-LEARN-DOCKER-SGN(NLD-SGN) is a dockerized application programming interface developed with [Flask](https://dormousehole.readthedocs.io/en/latest/), allowing users to run Schizo_Graph_Net models via the user interface provided by NEURO-LEARN-WEB.

### Start ```raniac/neuro-learn-service:sgn``` Container

```bash
$ docker run -it --rm --network host raniac/neuro-learn-service:sgn
```

### Build ```raniac/neuro-learn-service:sgn``` Image

```bash
$ docker build -t raniac/neuro-learn-service:sgn .
```

### Initiate ```raniac/neuro-learn-service:sgn``` Container for Dev

```bash
$ docker run -it --rm --network host -v /home/raniac/dev/NEURO-LEARN-DOCKER/services/sgn:/nls-sgn raniac/neuro-learn-service:sgn /bin/bash
```

### Design

#### Overview

This project aims to containerize/dockerize Schizo_Graph_Net as a service of NEURO-LEARN, developed with Flask.

- Expose new_task api so as to create new deep learning task utilizing SGN;
- SGN is developed with Pytorch and Pytorch_Geometric;
- Include Train-From-Scratch and Fine-Tune(use trained-model parameters);
- Incorporate DAO in order to perform CRUD on database, including insert_new_task, update_task_result, get_data, and get_model;
- Use Celery for queued task execution, along with Redis as cache backend;
- As for deployment, utilize Nginx as Reverse Proxy and Gunicorn as Load Balancing;
- Local deployment and container management are realized with docker-compose;
- Clustered computing services are implemented by kubernetes;

#### API Definition

##### *New Task*

- Request Information
  - Address: ```/rest/sgnservice/v0/new_sgn_task```
  - Method: POST
- Response Information
  - Type: HTTP
  - Content:
    - ```error_num```: request status
    - ```msg```: request result
    - ```task_form```: task form info
- Parameter Definition:

Parameter Name | Description | Necessary | Type | Default Value
:-: | :-: | :-: | :-: | :-:
```task_name``` | Task Name | True | STRING |
```task_type``` | Task Type | True | STRING |
```proj_id``` | Project ID | True | STRING |
```proj_name``` | Task Name | True | STRING |
```train_data``` | Train Data | True | STRING |
```val_data``` | Train Data | True | STRING |
```enable_test``` | Enable Test | True | BOOLEAN |
```test_data``` | Test Data | True | STRING |
```model``` | Model | True | STRING |
```param_set:learning_rate``` | Learning Rate | True | STRING |
```param_set:batch_size``` | Batch Size | True | STRING |
```param_set:lr_step_size``` | LR Step Size | True | STRING |
```param_set:lr_decay``` | LR Decay | True | STRING |
```param_set:epochs``` | Epochs | True | STRING |
```param_set:trained_task_id``` | Trained Task ID | True | STRING |
```param_set:save_model_state``` | Save Model State | True | BOOLEAN |

- POST Form Example

```json
{
    "proj_id":"PROJ20191217104136",
    "proj_name":"SZ with sfMRI",
    "task_name":"test",
    "task_type":"dl_ft",
    "train_data":["A_181210_140_SZ_sfMRI_AAL90"],
    "val_data":["A_181210_140_SZ_sfMRI_AAL90"],
    "enable_test":true,
    "test_data":["A_181210_140_SZ_sfMRI_AAL90"],
    "model":"GNN",
    "param_set": {
        "learning_rate": 5e-2,
        "batch_size": 10,
        "lr_step_size": 60,
        "lr_decay": 0.2,
        "epochs": 1,
        "trained_task_id": "TASK20012912454500",
        "save_model_state": false
    }
}
```
