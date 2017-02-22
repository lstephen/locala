#!/bin/bash

set -e
set -x

if [[ $(which pip) == '' ]];
then
  sudo /usr/bin/easy_install pip==9.0.1
  pip install ansible==2.2.1.0
  sudo rm /usr/local/bin/pip*
else
  pip install ansible==2.2.1.0
fi

ansible-playbook all.yml $ANSIBLE_FLAGS
