#!/bin/sh
set -e -x

cd /io

echo "============================================================"

for PYBIN in /opt/python/*/bin
do
   "${PYBIN}/python" inspecter.py
done

echo "============================================================"

for PYBIN in /opt/python/*/bin
do
   "${PYBIN}/python" setup.py build_ext -i
   ls
   "${PYBIN}/python" testit.py
done
