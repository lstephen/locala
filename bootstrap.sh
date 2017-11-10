#!/bin/bash

set -e
set -x

if [[ $(which brew) == '' ]]
then
  /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
fi

brew install gnu-tar python2
pip2 install ansible==2.2.1.0
ansible-playbook all.yml $ANSIBLE_FLAGS
