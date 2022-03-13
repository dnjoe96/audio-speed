#!/usr/bin/env bash

if [ $# -eq 1 ]
then
  if [ $1 = "--help" ]
  then
    echo 'USAGE:  ' + './' + $0 + ' authKey'
    exit 0
  fi

  auth=$1

  # install requirement
  pip3 install -r requirements.txt

  # ensure app.py is executable
  chmod u+x app.py

  # set AUTH_KEY
  export AUTH_KEY=$auth
  echo $AUTH_KEY
  exit 0

else
  echo 'please provide API Authentication key'
  exit 1
fi