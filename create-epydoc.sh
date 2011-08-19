#!/bin/bash

cd $(dirname $0)
mkdir -p ./docu/epydoc
epydoc -v --parse-only --html --no-frames -o ./docu/epydoc ./src/prctljail.py
