#!/bin/sh
set -e -x

cd /io

echo "============================================================"

for PYBIN in /opt/python/*/bin
do
   "${PYBIN}/python" socketinterrupted.py
done
