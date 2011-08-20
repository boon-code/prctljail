#!/bin/bash

cd $(dirname $0)
rm -rf ./sphinx/_build
find ./src/ -name "*.pyc" -exec rm "{}" ";"
find ./unittests/ -name "*.pyc" -exec rm "{}" ";"
find . -name "*~" -exec rm "{}" ";"
