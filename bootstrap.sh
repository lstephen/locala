#!/bin/bash

set -e
set -x

if [[ $(which brew) == '' ]]
then
  /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
fi

echo "Updating brew..."
brew update

echo "Verifying brew..."
brew doctor || true

echo "Installing brew packages..."
brew bundle

echo "Packages not listed in Brewfile..."
brew bundle cleanup

eval "$(pyenv init -)"
pip3 install ansible==2.10.4

echo "Configuring..."
ansible-playbook all.yml $ANSIBLE_FLAGS

echo "Done."
