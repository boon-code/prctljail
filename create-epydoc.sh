#!/bin/bash

cd $(dirname $0)
mkdir -p ./doc/epydoc
sed "s/.. note::/:note:/g" ./src/prctljail.py >./src/prctljail.py.epydoc~
epydoc -v --parse-only --html --no-frames -o ./doc/epydoc ./src/prctljail.py.epydoc~
