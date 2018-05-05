#!/usr/bin/env python

from __future__ import print_function

import sys, os

if sys.platform == "win32":
    # DLLs have nothing like -rpath $ORIGIN or -install_name @loader_path
    # to let dtest find the demo library by itself, so we have to help
    # this along by adding ourselves to %PATH%
    os.environ['PATH'] += '%s%s'%(os.pathsep, os.path.dirname(__file__))
    print('PATH = ', os.environ['PATH'])

import dtest

V = dtest.foo()
print("foo", V)
sys.exit(not (V==42))
