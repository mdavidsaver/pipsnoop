#!/bin/sh
set -e -x

echo "============================================================"

for PYBIN in /opt/python/*/bin
do
   "${PYBIN}/python" /io/inspecter.py
done

echo "============================================================"

for PYBIN in /opt/python/*/bin
do
   "${PYBIN}/pip" install nose
   "${PYBIN}/python" setup.py build_ext -i
   "${PYBIN}/python" -m nose pipsnoop
done
