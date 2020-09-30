FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y python3 \
                        python3-dev \
                        python3-pip \
                        libcurl4-openssl-dev \
    && apt-get clean \
    && apt-get autoclean \
    && rm -rf /var/lib/apt/lists/*

RUN export LC_ALL=C.UTF-8 \
    && export LANG=C.UTF-8

ADD ./requirements.txt /tmp/

RUN pip3 install -r /tmp/requirements.txt -i https://pypi.doubanio.com/simple

CMD ["/bin/bash"]