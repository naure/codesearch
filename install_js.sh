#!/bin/bash
set -e

pushd web
npm install
bower install
grunt build
popd
