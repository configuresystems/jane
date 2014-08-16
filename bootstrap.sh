#!/usr/env bash


yum install -y git-core gcc python-setuptools python-crypto m2crypto python-devel sysstat vim
python virtualenv.py flask
flask/bin/pip install -r requirements.txt
flask/bin/python db_create.py
/usr/lib64/sa/sa2 -A
