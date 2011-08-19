#!/bin/bash

cd $(dirname $0)
rm -r ./docu/
find ./src/ -name "*.pyc" -exec rm "{}" ";"
find ./unittests/ -name "*.pyc" -exec rm "{}" ";"
