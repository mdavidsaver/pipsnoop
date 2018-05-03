#!/bin/sh
set -e -x

for PYBIN in /opt/python/*/bin
do
   "${PYBIN}/python" /io/inspect.py
done
