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
brew doctor

echo "Installing brew packages..."
brew bundle

echo "Packages not listed in Brewfile..."
brew bundle cleanup

pip2 install ansible==2.2.1.0

echo "Configuring..."
ansible-playbook $1 $ANSIBLE_FLAGS

echo "Done."
