#!/bin/sh

echo $@
BASEDIR=$(dirname "$0")
cd $BASEDIR
./venv/bin/gunicorn run:app $@
