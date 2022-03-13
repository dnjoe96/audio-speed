#!/usr/bin/env bash

auth=$1

# install requirement
pip3 install -r requirements.txt

# ensure app.py is executable
chmod u+x app.py

# set AUTH_KEY
export AUTH_KEY=$auth
echo $AUTH_KEY