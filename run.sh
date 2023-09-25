#!/bin/sh

if [ "$#" -eq 0 ]; then
  python -m rinhac -b /var/rinha/source.rinha.json
  python /var/rinha/source.rinha.pyc
else
  python -m rinhac "$@"
fi
