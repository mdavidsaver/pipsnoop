#!/bin/sh
set -e -x

xcode-select -v
gcc -v
clang -v

dotest() {
    echo "==================================================="
    "$@" -dM -E -x c++ test.cpp || true
}

echo "" > test.cpp

echo "MACOSX_DEPLOYMENT_TARGET=$MACOSX_DEPLOYMENT_TARGET"
dotest gcc
dotest clang

echo "#include <memory>" > test.cpp

export MACOSX_DEPLOYMENT_TARGET=10.9
dotest clang -std=c++11
dotest clang -std=c++11 -stdlib=libc++
unset MACOSX_DEPLOYMENT_TARGET

g++ -o shared_ptr_test shared_ptr_test.cpp && ./shared_ptr_test
clang++ -o shared_ptr_test shared_ptr_test.cpp && ./shared_ptr_test

clang++ -std=c++98 -o shared_ptr_test shared_ptr_test.cpp && ./shared_ptr_test
clang++ -std=c++11 -o shared_ptr_test shared_ptr_test.cpp && ./shared_ptr_test
clang++ -std=c++11 -stdlib=libc++ -o shared_ptr_test shared_ptr_test.cpp && ./shared_ptr_test


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
