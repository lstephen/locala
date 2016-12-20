#!/bin/bash

set -e
set -x

sudo easy_install pip==9.0.1
pip install ansible==2.2.0.0

ansible-playbook all.yml
