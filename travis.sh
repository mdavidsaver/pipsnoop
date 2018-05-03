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
   "${PYBIN}/pip" install nose
   "${PYBIN}/python" setup.py build_ext -i
   LD_LIBRARY_PATH="$PWD" "${PYBIN}/python" -m nose pipsnoop
done
