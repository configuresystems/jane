#!/usr/env bash


yum install -y git-core gcc python-setuptools python-crypto m2crypto python-devel
python virtualenv.py flask
flask/bin/pip install -r requirements.txt