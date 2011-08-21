#!/bin/bash

cd $(dirname $0)
mkdir -p ./doc/sphinx
cd sphinx
mkdir -p ./_static
mkdir -p ./_templates
make html
