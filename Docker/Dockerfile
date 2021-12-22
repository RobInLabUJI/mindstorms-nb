FROM jupyter/scipy-notebook:latest

USER root

RUN apt-get update && apt-get install -y \
      libbluetooth-dev \
    && rm -rf /var/lib/apt/lists/*

COPY ev3 work/ev3
COPY img work/img
COPY nxt work/nxt
COPY task work/task
COPY index.ipynb work/index.ipynb

RUN chown -R jovyan.users work

USER jovyan
    
RUN pip install pybluez rpyc

RUN python3 -m pip install --upgrade --pre nxt-python

RUN python3 -m pip install ev3_dc
