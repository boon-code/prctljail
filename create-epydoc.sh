#!/bin/bash

cd $(dirname $0)
mkdir -p ./doc/epydoc
epydoc -v --parse-only --html --no-frames -o ./doc/epydoc ./src/prctljail.py
