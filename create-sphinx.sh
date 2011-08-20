#!/bin/bash

cd $(dirname $0)
mkdir -p ./doc/sphinx
cd sphinx
make html
