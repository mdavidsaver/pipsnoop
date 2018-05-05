#!/bin/sh
set -e -x

xcode-select -v
gcc -v
clang -v

g++ -o shared_ptr_test1 shared_ptr_test.cpp && ./shared_ptr_test1
clang++ -o shared_ptr_test2 shared_ptr_test.cpp && ./shared_ptr_test2
/usr/bin/clang -fno-strict-aliasing -fno-common -dynamic -arch i386 -arch x86_64 -g -DNDEBUG -g -fwrapv -O3 -Wall -Wstrict-prototypes -o shared_ptr_test3 shared_ptr_test.cpp && ./shared_ptr_test3

# https://github.com/joerick/cibuildwheel/blob/master/cibuildwheel/macos.py

curl -L -o /tmp/Python.pkg $URL
curl -L -o /tmp/get-pip.py https://bootstrap.pypa.io/get-pip.py

sudo installer -pkg /tmp/Python.pkg -target /

export PATH=$PATH:/Library/Frameworks/Python.framework/Versions/$PYVER/bin

which $PYTHON

$PYTHON --version

$PYTHON /tmp/get-pip.py --no-setuptools --no-wheel

$PYTHON -m pip --version
$PYTHON -m pip install --upgrade setuptools
$PYTHON -m pip install --upgrade wheel

$PYTHON inspecter.py
$PYTHON setup.py build_ext -i -v
ls
otool -l libdemo.*
otool -l dtest.*
$PYTHON testit.py
