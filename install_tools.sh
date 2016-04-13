#!/bin/bash
set -e

apt-get install \
    wget make nginx \
    nodejs npm \
    python-pip python-dev \
    python-yaml python-django \
    ;

pip install -r requirements.txt
npm install -g grunt-cli
npm install -g bower
ln -sf nodejs /usr/bin/node
