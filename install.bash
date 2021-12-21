#!/bin/bash

sudo apt update
sudo apt install -y libbluetooth-dev

pip install jupyter matplotlib pybluez
python3 -m pip install --pre nxt-python
python3 -m pip install ev3_dc
