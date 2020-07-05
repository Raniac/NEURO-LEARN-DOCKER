# FROM ubuntu-with-python:dev
FROM imcomking/pytorch_geometric:latest

RUN apt-get update \
    && apt-get -y install redis-server \
    && apt-get clean \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/*

ADD . /workspace/

RUN pip install -r requirements.txt -i https://pypi.doubanio.com/simple

CMD ["/bin/bash"]